import httpx

def run_tests():
    client = httpx.Client(base_url='http://127.0.0.1:8000')

    # 1. Health
    r = client.get('/api/health')
    print('=== 1. HEALTH CHECK ===')
    print('Status:', r.status_code, r.json())
    assert r.status_code == 200

    # 2. Delhi Fashion Search (Mock)
    req_delhi = {
        'region': 'Delhi',
        'niche': 'Fashion',
        'followers_min': 10000,
        'followers_max': 100000,
        'keywords': ['model', 'creator'],
        'provider': 'mock',
        'max_results': 10
    }
    r_delhi = client.post('/api/search', json=req_delhi)
    print('\n=== 2. DELHI FASHION DISCOVERY ===')
    print('Status:', r_delhi.status_code)
    data_delhi = r_delhi.json()
    print('Total found:', data_delhi['total_found'], '| Latency:', data_delhi['execution_time_ms'], 'ms')
    print('Available tags:', data_delhi['available_tags'])
    print('Available regions:', data_delhi['available_regions'])

    top = data_delhi['profiles'][0]
    print('\nTop Profile:')
    print(' Username:', top['username'])
    print(' Display Name:', top['display_name'])
    print(' Followers:', top['followers_formatted'])
    print(' Region:', top['region'])
    print(' Tags:', top['tags'])
    print(' Match Score:', top['match_score'], '/ 100')
    print(' Match Reasons:')
    for reason in top['match_reasons']:
        print(f"  - {reason['criterion']}: {reason['description']} (+{reason['score_contribution']})")
    print(' Data Confidence:', top['data_confidence'])
    assert top['match_score'] >= 85

    # 3. Bangalore Tech Search
    req_bangalore = {
        'region': 'Bangalore',
        'niche': 'Technology',
        'followers_min': 10000,
        'followers_max': 500000,
        'keywords': ['developer', 'coding', 'ai'],
        'provider': 'mock',
        'max_results': 10
    }
    r_blr = client.post('/api/search', json=req_bangalore)
    print('\n=== 3. BANGALORE TECH DISCOVERY ===')
    data_blr = r_blr.json()
    print('Total found:', data_blr['total_found'])
    top_blr = data_blr['profiles'][0]
    print('Top Profile:', top_blr['username'], '| Score:', top_blr['match_score'], '| Tags:', top_blr['tags'])
    assert top_blr['match_score'] >= 80

    # 4. Live Search Provider Test (Auto / Search)
    print('\n=== 4. LIVE SEARCH DISCOVERY TEST ===')
    req_live = {
        'region': 'Delhi',
        'niche': 'Fashion',
        'keywords': ['model'],
        'provider': 'auto',
        'max_results': 5
    }
    r_live = client.post('/api/search', json=req_live)
    print('Status:', r_live.status_code)
    data_live = r_live.json()
    print('Provider used:', data_live['provider_used'], '| Total found:', data_live['total_found'], '| Is Demo:', data_live['is_demo'])

    # 5. CSV Export Test
    search_id = data_delhi['search_id']
    r_csv = client.get(f'/api/export/{search_id}?format=csv')
    print('\n=== 5. CSV EXPORT VERIFICATION ===')
    print('Status:', r_csv.status_code)
    print('Content-Type:', r_csv.headers.get('content-type'))
    csv_lines = r_csv.text.strip().split('\n')
    print('CSV Header:', csv_lines[0])
    print('CSV Row 1:', csv_lines[1] if len(csv_lines) > 1 else 'None')
    assert "Username,Profile URL" in csv_lines[0]

    # 6. Profile Lookup Test
    username = top['username']
    r_prof = client.get(f'/api/profile/{username}')
    print('\n=== 6. PROFILE LOOKUP ===')
    print('Status:', r_prof.status_code, '| Username:', r_prof.json()['username'])
    assert r_prof.status_code == 200

    print('\n=============================================')
    print('>>> ALL 6 END-TO-END TESTS PASSED SUCCESSFULLY! <<<')
    print('=============================================')

if __name__ == '__main__':
    run_tests()
