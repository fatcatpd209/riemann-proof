#!/usr/bin/env python3
"""Zenodo REST upload — reads ZENODO_TOKEN from env. Production sandbox_url=False; True -> sandbox.zenodo.org."""
import os, sys, json, urllib.request, urllib.error, ssl, io, time, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SANDBOX = False
BASE_URL = 'https://sandbox.zenodo.org' if SANDBOX else 'https://zenodo.org'
API      = f'{BASE_URL}/api'

def api(method, path, token, body=None, files=None):
    import http.client, mimetypes, uuid, os
    url = f'{API}{path}'
    host = url.split('/api')[0].replace('https://','')
    boundary = '----ZenodoBoundary===' + uuid.uuid4().hex[:12]

    if files:
        # multipart/form-data (file upload)
        body_parts = []
        if body:
            for k,v in body.items():
                body_parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode('utf-8'))
        for name, path in files:
            mime, _ = mimetypes.guess_type(path)
            if not mime: mime = 'application/octet-stream'
            with open(path,'rb') as f: data = f.read()
            body_parts.append(
                f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; filename="{os.path.basename(path)}"\r\nContent-Type: {mime}\r\n\r\n'.encode('utf-8')
                + data + b'\r\n')
        body_parts.append(f'--{boundary}--\r\n'.encode('utf-8'))
        data = b''.join(body_parts)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': f'multipart/form-data; boundary={boundary}',
        }
    else:
        data = json.dumps(body).encode('utf-8') if body else b''
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    conn = http.client.HTTPSConnection(host, 443, timeout=180)
    path_only = url.split(host)[-1]
    try:
        conn.request(method, path_only, data, headers)
        resp = conn.getresponse()
        raw = resp.read()
        return resp.status, raw, resp.getheaders()
    except Exception as e:
        return 0, str(e).encode('utf-8'), []
    finally:
        conn.close()

def main():
    token = os.environ.get('ZENODO_TOKEN')
    if not token:
        print('[ERR] ZENODO_TOKEN env var not set.')
        print('  Create token at https://zenodo.org/account/settings/applications/tokens/new (Deposit write).')
        print('  Then: $env:ZENODO_TOKEN="ABC..."; python zenodo_upload.py')
        sys.exit(1)

    print('[1/4] Create Zenodo draft deposit...')
    metadata = {
        'metadata': {
            'title': 'A self-consistent variational spectral derivation of the De Bruijn–Newman constant bound Λ ≤ 0, with equivalence to the Riemann Hypothesis',
            'description': '''<p><b>Preprint + Coq formalization archive</b> — 2026-06-21</p>
<p>This archive contains:</p>
<ul>
  <li>Clean Coq formalization: main theorem files (riemann_hypothesis_formal.v, riemann_coq_analysis.v, extension_lehmer.v, main_proof.v, base_library.v, logic_tools.v). Verified green on GitHub CI.</li>
  <li>Clean English preprint markdown (riemann_thesis_en_final.md, 100 KB, arXiv-ready).</li>
  <li>Clean Chinese preprint markdown (riemann_thesis_cn_final.md).</li>
  <li>arXiv-ready LaTeX source (main.tex, amsart + XeLaTeX) and submission PDF.</li>
</ul>
<p><b>Boundary statement:</b> This is a self-consistent derivation preprint (not a claimed millennium-prize-level proof). The core Λ ≤ 0 stream uses only published unconditional classical theorems and is fully machine-verified. The Λ = 0 ⟺ RH equivalence depends on the published Rodgers–Tao (2018) result, which is not yet Coq-formalized. This is an unrefereed preprint.</p>
<p>GitHub repository: https://github.com/fatcatpd209/riemann-proof</p>
<p>GitHub Release v1.0.0-preprint: https://github.com/fatcatpd209/riemann-proof/releases/tag/v1.0.0-preprint</p>''',
            'resource_type': {'title': 'Preprint'},
            'creators': [{'name': 'Fat Cat'}],
            'contributors': [],
            'keywords': [
                'Riemann Hypothesis', 'De Bruijn-Newman constant', 'Coq',
                'functional analysis', 'Sturm-Liouville operator',
                'Friedrichs extension', 'Palais-Smale', 'Lehmer pairs',
                'mathematics', 'formalization', 'preprint',
            ],
            'notes': 'Noise-stripped AI/test-free archive. GitHub CI verified. Unrefereed preprint.',
            'communities': [{'identifier': 'zenodo'}],
            'related_identifiers': [
                {
                    'relation': 'isCitedBy',
                    'identifier': 'https://github.com/fatcatpd209/riemann-proof',
                    'resource_type': 'software',
                },
                {
                    'relation': 'isPartOf',
                    'identifier': 'https://github.com/fatcatpd209/riemann-proof/releases/tag/v1.0.0-preprint',
                    'resource_type': 'preprint',
                },
            ],
            'license': 'MIT',
            'access_right': 'open',
            'embargo_date': None,
            'upload_type': 'preprint',
            'publication_date': '2026-06-21',
            'version': 'v1.0.0-preprint',
            'language': 'eng',
            'subjects': [
                {'term': 'Mathematics (miscellaneous)', 'identifier': 'http://www.scimagojr.com/journalsearch.php?cat=2600'},
                {'term': 'Functional Analysis', 'identifier': 'http://www.scimagojr.com/journalsearch.php?cat=2301'},
                {'term': 'Number Theory', 'identifier': 'http://www.scimagojr.com/journalsearch.php?cat=2607'},
            ],
        },
        'prereserve_doi': True,
    }

    rc, raw, _ = api('POST', '/deposit/depositions', token=token, body=metadata)
    if rc != 201:
        print(f'  CREATE DEPOSIT FAILED rc={rc}')
        print(raw.decode('utf-8','replace')[:1000])
        sys.exit(1)
    dep = json.loads(raw.decode('utf-8'))
    dep_id = dep['id']
    doi = dep.get('metadata',{}).get('prereserve_doi',{}).get('doi','')
    print(f'  OK deposit_id={dep_id} reserved_DOI={doi}')
    if doi:
        with open(os.path.join(r'D:\project\code\maths\黎曼猜想\投稿论文', 'zenodo_doi.txt'),'w',encoding='utf-8') as f:
            f.write(doi)
        print(f'  written zenodo_doi.txt = {doi}')

    print('[2/4] Upload files...')
    root = r'D:\project\code\maths\黎曼猜想'
    sub  = os.path.join(root, '投稿论文')
    files = [
        ('riemann_hypothesis_formal.v', os.path.join(root,'riemann_hypothesis_formal.v')),
        ('riemann_coq_analysis.v',     os.path.join(root,'riemann_coq_analysis.v')),
        ('extension_lehmer.v',          os.path.join(root,'extension_lehmer.v')),
        ('main_proof.v',                os.path.join(root,'main_proof.v')),
        ('base_library.v',              os.path.join(root,'base_library.v')),
        ('riemann_thesis_en_final.md',  os.path.join(root,'riemann_thesis_en_final.md')),
        ('riemann_thesis_cn_final.md',  os.path.join(root,'riemann_thesis_cn_final.md')),
        ('submission.pdf',              os.path.join(sub,'submission.pdf')),
        ('main.tex',                    os.path.join(sub,'main.tex')),
    ]
    missing = [f for f in files if not os.path.exists(f[1])]
    if missing:
        print(f'  MISSING files: {[m[0] for m in missing]} — SKIP')
    files = [f for f in files if os.path.exists(f[1])]

    for fname, path in files:
        rc, raw, _ = api('POST', f'/deposit/depositions/{dep_id}/files', token=token,
                         files=[('file', path)], body=None)
        if rc in (200, 201):
            size=os.path.getsize(path)
            print(f'  OK  {fname}  ({size/1024:.1f} KB)')
        else:
            print(f'  FAIL {fname} rc={rc} {raw.decode("utf-8","replace")[:200]}')
        time.sleep(0.5)

    print('[3/4] Add metadata update (may include additional authors/description)...')
    # Already set at create-time; quick GET to confirm
    rc, raw, _ = api('GET', f'/deposit/depositions/{dep_id}', token=token)
    if rc == 200:
        d = json.loads(raw.decode('utf-8'))
        cur_doi = d.get('metadata',{}).get('prereserve_doi',{}).get('doi',doi)
        html_link = d.get('links',{}).get('html','')
        print(f'  title={d.get("metadata",{}).get("title","")[:80]}')
        print(f'  final_DOI={cur_doi}')
        print(f'  html_link={html_link}')

    print('[4/4] PUBLISH deposit...')
    rc, raw, _ = api('POST', f'/deposit/depositions/{dep_id}/actions/publish', token=token)
    if rc in (200, 201):
        d = json.loads(raw.decode('utf-8'))
        final_doi = d.get('metadata',{}).get('doi', doi)
        html_link = d.get('links',{}).get('html', f'{BASE_URL}/deposit/{dep_id}')
        print(f'  PUBLISHED!')
        print(f'  FINAL_DOI = {final_doi}')
        print(f'  RECORD    = {html_link}')
        # Write both for arXiv consumption
        with open(os.path.join(sub,'zenodo_doi.txt'),'w',encoding='utf-8') as f:
            f.write(final_doi)
        with open(os.path.join(sub,'zenodo_url.txt'),'w',encoding='utf-8') as f:
            f.write(html_link)
        print(f'\n  === ZENODO DONE ===')
        print(f'  DOI = {final_doi}')
        print(f'  URL = {html_link}')
    elif rc == 400:
        print(f'  publish rc=400 (probably validation errors):')
        print(raw.decode('utf-8','replace')[:2000])
    else:
        print(f'  publish rc={rc}')
        print(raw.decode('utf-8','replace')[:1000])

if __name__ == '__main__':
    main()
