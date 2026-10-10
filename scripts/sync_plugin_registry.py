#!/usr/bin/env python3
"""Project one public plugin-registry commit into the Working Tools catalog."""
import argparse,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('checkout',type=Path);p.add_argument('revision');a=p.parse_args()
def git(*args):return subprocess.check_output(['git','-C',str(a.checkout),*args],text=True)
remote=git('remote','get-url','origin').strip()
if remote.removesuffix('.git')!='https://github.com/JonathanKHobson/working-tools-plugins':raise SystemExit('Expected the public Working Tools Plugins source')
sha=git('rev-parse',a.revision+'^{commit}').strip();data=json.loads(git('show',sha+':catalog/packages.json'))
items=[]
site_root=Path(__file__).resolve().parents[1]
merch=json.loads((site_root/'data/storefront-copy.json').read_text())
excluded=set(merch.get('excluded_ids',[]))
for r in data['packages']:
 if r['distribution']!='released' or r['id'] in excluded:continue
 if r['id'] not in merch['products']:raise SystemExit('Missing storefront copy for released package: '+r['id'])
 names=git('ls-tree','-r','--name-only',sha,'plugins/'+r['id']+'/skills').splitlines()
 skills=[re.search(r'^name:\s*(.+)$',git('show',sha+':'+n),re.M)[1] for n in names if n.endswith('/SKILL.md')]
 manifest=json.loads(git('show',sha+':plugins/'+r['id']+'/.codex-plugin/plugin.json'))
 display_name=manifest.get('interface',{}).get('displayName',r['name'])
 item={k:r[k] for k in ['id','version','description','requirements','edition','license']}
 item['name']=display_name
 job_aliases={'market':'write','play':'table'}
 jobs=list(dict.fromkeys(job_aliases.get(job,job) for job in r.get('jobs',['build'])))
 item.update(merch['products'][r['id']],skill_names=skills,jobs=jobs,release_url='https://github.com/JonathanKHobson/working-tools-plugins/releases/tag/'+r['id']+'/v'+r['version'])
 items.append(item)
output={'schema_version':'working-tools.plugins.v1','source_repository':remote,'source_revision':sha,'packages':items}
site_root.joinpath('data/plugin-releases.json').write_text(json.dumps(output,indent=2)+'\n')
print(f'Projected {len(items)} released packages from {sha}')
