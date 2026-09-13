"""Import a Notion Markdown export without changing technical prose or example code.

Usage: python scripts/import_guides.py --source PATH
Source edits should be made in Notion; generated pages may be regenerated.
"""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, quote

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    ('main', 'index.md', 'Overview', '/', 1, None),
    ('매뉴얼00', 'v1.3/getting-started.md', 'Getting Started', '/v1.3/getting-started/', 2, None),
    ('매뉴얼01', 'v1.3/task-owner/create-task.md', 'Create a New Task', '/v1.3/task-owner/create-task/', 1, 'Task Owner'),
    ('매뉴얼02', 'v1.3/task-owner/import-model.md', 'Import a Local Model', '/v1.3/task-owner/import-model/', 2, 'Task Owner'),
    ('매뉴얼03', 'v1.3/participant.md', 'Participant: Join & FL', '/v1.3/participant/', 4, None),
    ('매뉴얼04', 'v1.3/agent-builder.md', 'Agent Builder & Serving', '/v1.3/agent-builder/', 5, None),
    ('매뉴얼05', 'v1.3/campaign.md', 'Campaign & Server Management', '/v1.3/campaign/', 6, None),
    ('개발자가이드', 'v1.3/developer-guide.md', 'Federated Task Developer Guide', '/v1.3/developer-guide/', 7, None),
]

def link(url):
    return "{{ '" + url + "' | relative_url }}"

def fix_tables(text):
    lines = text.splitlines()
    result=[]
    i=0
    while i < len(lines):
        line=lines[i]
        if line.lstrip().startswith('|') and not line.rstrip().endswith('|'):
            while i+1<len(lines) and not line.rstrip().endswith('|') and lines[i+1].strip():
                i+=1
                line += '<br>' + lines[i].strip()
        result.append(line)
        i+=1
    return '\n'.join(result)

def protect_code(text):
    """Extract nested exported fences; HTML-escape code so Liquid never executes it."""
    lines=text.splitlines(keepends=True)
    blocks=[]
    output=[]
    i=0
    while i<len(lines):
        m=re.match(r'^(\s*)(`{3,})([^\n]*)\n?$',lines[i])
        if not m:
            output.append(lines[i]); i+=1; continue
        indent=m[1]; language=m[3].strip(); stack=[language]; payload=[]; i+=1
        while i<len(lines):
            line=lines[i]; f=re.match(r'^\s*`{3,}([^\n]*)\n?$',line)
            if f:
                lang=f[1].strip()
                if lang and stack[-1] in ('markdown','md'):
                    stack.append(lang)
                elif not lang:
                    stack.pop()
                    if not stack:
                        i+=1; break
            payload.append(line[len(indent):] if line.startswith(indent) else line)
            i+=1
        if stack:
            raise ValueError('Unclosed code block: '+language)
        # Longer fence preserves Markdown examples which contain their own fences.
        code=''.join(payload).rstrip('\n')
        fence='`' * max(3, max([len(x) for x in re.findall(r'`+',code)]+[0])+1)
        block=indent+fence+language+'\n'+''.join(indent+l+'\n' for l in code.split('\n'))+indent+fence+'\n'
        # Protect only Liquid delimiters if present, while preserving the displayed code.
        block=re.sub(r'\{\{|\{%', lambda m: '{% raw %}'+m[0]+'{% endraw %}', block)
        token=f'FEDOPSCODEBLOCK{len(blocks):04}TOKEN'
        blocks.append(block)
        output.append(token+'\n')
    return ''.join(output),blocks

def run(source):
    files={row[0]:next((source/row[0]).glob('*.md')) for row in PAGES}
    ids={re.search(r'([a-f0-9]{32})',f.name)[1]:row[3] for row in PAGES for f in [files[row[0]]]}
    manual_urls={f'{i:02}':PAGES[i+1][3] for i in range(6)}
    manifest=[]
    notes=[]
    for group,dest,title,url,order,parent in PAGES:
        f=files[group]; original=f.read_text(encoding='utf-8-sig')
        text,blocks=protect_code(original)
        if group=='main':
            text=text.replace('중심이이었다', '중심이었다')
            # Editorial tasks and backup links remain in the local review document.
            text,editorial=text.split('# 상세 시나리오 매뉴얼',1)
            notes.append('## Main의 편집 메모 및 원본 링크\n\n'+editorial)
        text=re.sub(r'^# .*\n\s*','',text,count=1)
        text=re.sub(r'^# (.*)\n',lambda m: m[1]+'\n{: .fs-5 .fw-400 }\n',text,count=1)
        def headings(m):
            hashes,label=m[1],m[2]
            if group=='main': return m[0]
            if group=='개발자가이드' and re.match(r'\d+\.',label): return '## '+label
            return '#'*min(6,len(hashes)+1)+' '+label
        text=re.sub(r'^(#{1,6}) (.+)$',headings,text,flags=re.M)
        text=fix_tables(text)
        asset_count=0
        def image_ref(m):
            nonlocal asset_count
            rel=unquote(m[2]); image_file=(f.parent/rel).resolve()
            if not image_file.is_file(): raise FileNotFoundError(image_file)
            slug='overview' if group=='main' else ('developer-guide' if group=='개발자가이드' else 'manual-'+group[-2:])
            name=image_file.name.replace(' ','-')
            asset_url=f'/assets/images/v1.3/{slug}/{name}'
            target=ROOT/asset_url.lstrip('/'); target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(image_file,target); asset_count+=1
            return f'![{m[1]}]({link(quote(asset_url,safe="/"))})'
        text=re.sub(r'!\[([^\]]*)\]\(([^\n)]+)\)',image_ref,text)
        for id_,target in ids.items():
            text=re.sub(r'https://(?:app\.notion\.com|[^/]+\.notion\.site|www\.notion\.so)/[^\s)]*'+id_+r'[^\s)]*',lambda _:link(target),text)
        # Turn prose references and table cells into real links, without nesting existing links.
        for num,target in manual_urls.items():
            text=text.replace('`매뉴얼 '+num+'`',f'[매뉴얼 {num}]({link(target)})')
            text=re.sub(r'(?<![\w\[])매뉴얼 '+num+r'(?=의|을|를|\s*\|)',lambda _:f'[매뉴얼 {num}]({link(target)})',text)
        # Match destinations, not old labels: Notion titles may contain IDs or typos.
        for _,_,label,target,_,_ in PAGES:
            destination='('+link(target)+')'
            text=re.sub(r'(?<!!)\[[^\]\n]+\]'+re.escape(destination),
                        lambda _,label=label,destination=destination: '['+label+']'+destination,text)
        text=re.sub(r'(\]\(\{\{[^\n]+?\}\}\))\s*(?:을|를) 따른다\.',r'\1 문서를 따른다.',text)
        if group=='개발자가이드':
            start=text.index('- MNIST/')
            end=text.index('![image.png]')
            examples=text[start:end]
            text=text[:start]+'<details markdown="1" class="guide-examples">\n<summary>MNIST 완성 예제와 Baseline 코드 보기</summary>\n\n'+examples+'\n</details>\n\n'+text[end:]
        for i,block in enumerate(blocks): text=text.replace(f'FEDOPSCODEBLOCK{i:04}TOKEN\n',block)
        text=re.sub(r'^\|\s*\|\s*\|\s*$', '', text,flags=re.M)
        fm={'layout':'default','title':title,'nav_order':order,'permalink':url,'docs_version':'1.3','lang':'ko','guide_source':f.name,'guide_status':'draft'}
        if parent:fm['parent']=parent
        if group=='매뉴얼02':fm['guide_note']='작성 중: 기존 Local Model 전환 절차는 보완이 필요한 초안입니다.'
        if group=='매뉴얼01':fm['guide_note']='검토 중: Web Draft 정의 등 원문의 작성 메모가 남아 있습니다.'
        if group=='매뉴얼05':fm['guide_note']='검토 중: Campaign 저장과 서버 생성 순서를 확인해야 합니다.'
        front='---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in fm.items())+'\n---\n\n'
        page=front+'# '+title+'\n{: .no_toc }\n\n'+text.strip()+'\n'
        target=ROOT/dest; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(page,encoding='utf-8')
        manifest.append({'source':str(f.relative_to(source)),'sha256':hashlib.sha256(original.encode()).hexdigest(),'output':dest,'images':asset_count,'code_blocks':len(blocks)})
    (ROOT/'_data').mkdir(exist_ok=True)
    (ROOT/'_data/guide_import.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'GUIDE_EDITORIAL_NOTES.md').write_text('# 1.3 가이드 편집 메모\n\n사이트 본문과 분리한 원본 메모입니다. 내용 확정 후 Notion 원본에서 수정하고 다시 이관합니다.\n\n'+'\n'.join(notes)+'\n\n## 추가 검토 항목\n\n- Main은 Tool AI 1개 이상, Manual 04는 0개 이상으로 설명합니다. 원문을 보존했으며 최소 개수 정책 확인이 필요합니다.\n- Manual 01/03의 데이터 경로 안내를 Developer Guide의 data_root 계약과 대조해야 합니다.\n- Manual 02는 작성 중입니다.\n- Manual 05의 Campaign 저장·서버 생성 순서를 확인해야 합니다.\n',encoding='utf-8')
    print(f'Imported {len(manifest)} guides; {sum(x["images"] for x in manifest)} image references; {sum(x["code_blocks"] for x in manifest)} code blocks.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--source',type=Path,required=True)
    run(parser.parse_args().source.resolve())
