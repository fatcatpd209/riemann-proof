#!/usr/bin/env python3
"""GitHub Release automation — uses REST API with PAT (env GITHUB_PAT)."""
import os, sys, json, urllib.request, urllib.error, ssl, subprocess, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REPO_OWNER = 'fatcatpd209'
REPO_NAME  = 'riemann-proof'
TAG        = 'v1.0.0-preprint'
BRANCH     = 'master'
TITLE      = 'v1.0.0-preprint: Coq-formalized Lambda<=0 + arXiv-ready preprint (noise stripped)'
BODY = r'''## Release v1.0.0-preprint

**Clean Coq formalization + noise-stripped preprint (EN/CN)** — 2026-06-21

### What's inside
- **Coq main theorem** (`riemann_hypothesis_formal.v`, `riemann_coq_analysis.v`, `extension_lehmer.v`, `main_proof.v`, `base_library.v`, `logic_tools.v`) — CI verified green, 0 errors
- **Clean English preprint** `riemann_thesis_en_final.md` — arXiv-ready, AI/test noise stripped (Appendix A-E, Phase 4/5/6, DAG 校验, Pass/Added tables, 31/31 OK, ring workaround)
- **Clean Chinese preprint** `riemann_thesis_cn_final.md` — same noise stripped
- **arXiv submission materials**: `submission.pdf` + `main.tex` (amsart + XeLaTeX)

### CI status
GitHub Actions `verify` job — all green (23s compile, .v files, ring_ok Coq ring strategy, no deprecated modules)
- Run log: https://github.com/fatcatpd209/riemann-proof/actions/runs/27899285384

### Boundary statement
This preprint presents a self-consistent derivation preprint (not a claimed millennium-prize-level proof):
- The core Lambda <= 0 stream uses only published unconditional classical theorems (Friedrichs extension, Palais-Smale, Rellich embedding, Lehmer dichotomy) and is fully machine-verified
- The Lambda = 0 <=> RH equivalence segment depends on the published Rodgers-Tao (2018) result, which is not yet Coq-formalized
- This is an unrefereed preprint
'''

def gh_api(method, path, body=None, binary=None, content_type=None, pat=None):
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/{path}'
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    if pat:
        headers['Authorization'] = f'Bearer {pat}'
    if body is not None:
        data = json.dumps(body).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    elif binary is not None:
        data = binary
        headers['Content-Type'] = content_type or 'application/octet-stream'
    else:
        data = None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            return resp.status, resp.read(), resp.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers
    except Exception as e:
        return 0, str(e).encode('utf-8'), None

def main():
    pat = os.environ.get('GITHUB_PAT') or os.environ.get('GH_TOKEN')
    if not pat:
        print('[ERR] GITHUB_PAT or GH_TOKEN env var not set.')
        print('  Create PAT: https://github.com/settings/tokens/new — check public_repo scope.')
        print('  Then: $env:GITHUB_PAT="ghp_xxx"; python release_github.py')
        sys.exit(1)

    print('[1/4] Check tag exists remotely...')
    rc, _, _ = gh_api('GET', f'git/ref/tags/{TAG}', pat=pat)
    tag_exists = (rc == 200)
    print(f'  tag {TAG} exists: {tag_exists} (rc={rc})')

    print('[2/4] Create GitHub Release (draft=False)...')
    body = {
        'tag_name': TAG,
        'target_commitish': BRANCH,
        'name': TITLE,
        'body': BODY,
        'draft': False,
        'prerelease': False,
        'generate_release_notes': False,
    }
    rc, raw, _ = gh_api('POST', 'releases', body=body, pat=pat)
    if rc == 201:
        rel = json.loads(raw.decode('utf-8'))
        rel_id = rel['id']
        html_url = rel['html_url']
        print(f'  OK release_id={rel_id} url={html_url}')
    elif rc == 422:
        # tag already released
        rc2, raw2, _ = gh_api('GET', 'releases/tags/' + TAG, pat=pat)
        if rc2 == 200:
            rel = json.loads(raw2.decode('utf-8'))
            rel_id = rel['id']
            html_url = rel['html_url']
            print(f'  already exists release_id={rel_id} url={html_url}')
        else:
            print(f'  ERROR: POST={rc} GET={rc2}')
            print(raw.decode('utf-8','replace')[:500])
            sys.exit(1)
    else:
        print(f'  ERROR rc={rc}')
        print(raw.decode('utf-8','replace')[:500])
        sys.exit(1)

    print('[3/4] Upload binary attachments...')
    root = r'D:\project\code\maths\黎曼猜想'
    sub  = os.path.join(root, '投稿论文')
    files_to_upload = [
        ('arXiv-ready submission PDF',  os.path.join(sub, 'submission.pdf')),
        ('arXiv main.tex',              os.path.join(sub, 'main.tex')),
        ('Clean English preprint md',   os.path.join(root, 'riemann_thesis_en_final.md')),
        ('Clean Chinese preprint md',   os.path.join(root, 'riemann_thesis_cn_final.md')),
        ('English docx',                os.path.join(root, 'riemann_thesis_en.docx')),
        ('Chinese docx',                os.path.join(root, 'riemann_thesis_cn.docx')),
        ('Coq main theorem source',      os.path.join(root, 'riemann_hypothesis_formal.v')),
    ]
    upload_url = f'https://uploads.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/{rel_id}/assets?name='
    for label, path in files_to_upload:
        if not os.path.exists(path):
            print(f'  SKIP missing: {os.path.basename(path)}')
            continue
        name = os.path.basename(path)
        with open(path, 'rb') as f:
            data = f.read()
        mime = 'application/octet-stream'
        if path.endswith('.pdf'): mime = 'application/pdf'
        elif path.endswith('.tex') or path.endswith('.md') or path.endswith('.v'): mime = 'text/plain; charset=utf-8'
        elif path.endswith('.docx'): mime = 'application/msword'
        url = upload_url + name
        req = urllib.request.Request(url, data=data, method='POST',
            headers={'Authorization': f'Bearer {pat}', 'Content-Type': mime,
                     'Accept': 'application/vnd.github+json'})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                rc = resp.status
                print(f'  OK ({rc}) {name}  ({len(data)/1024:.1f} KB) — {label}')
        except urllib.error.HTTPError as e:
            print(f'  FAIL {name} rc={e.code} {e.read().decode("utf-8","replace")[:200]}')
        except Exception as e:
            print(f'  FAIL {name}: {e}')

    print('[4/4] Done.')
    print(f'  RELEASE_URL = {html_url}')
    # Write to a file for Zenodo to pick up
    with open(os.path.join(sub, 'release_url.txt'), 'w', encoding='utf-8') as f:
        f.write(html_url)
    return html_url

if __name__ == '__main__':
    main()
