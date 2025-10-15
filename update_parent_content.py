#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
상위기능명 -> 상위요구사항내용으로 변경하고
상위기능ID의 요구사항내용을 자동으로 채우는 스크립트
"""

import json
import sys

def update_json_file(input_file, output_file):
    """JSON 파일 업데이트"""
    
    # 1. JSON 파일 읽기
    print(f"[INFO] 파일 읽는 중: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] 파일 읽기 실패: {e}")
        return False
    
    print(f"[OK] {len(data)}개 요구사항 로드됨")
    
    # 2. 기능ID로 요구사항 매핑 (빠른 검색을 위해)
    req_map = {}
    for req in data:
        func_id = req.get('기능ID', '')
        if func_id:
            req_map[func_id] = req
    
    # 3. 각 요구사항 업데이트
    updated_count = 0
    field_renamed_count = 0
    
    for req in data:
        # 3-1. "상위기능명" -> "상위요구사항내용" 필드명 변경
        if '상위기능명' in req:
            req['상위요구사항내용'] = req.pop('상위기능명')
            field_renamed_count += 1
        
        # 3-2. 상위기능ID가 있으면 해당 요구사항내용 가져오기
        parent_id = req.get('상위기능ID', '')
        if parent_id and parent_id in req_map:
            parent_req = req_map[parent_id]
            parent_content = parent_req.get('요구사항내용', '')
            
            if parent_content:
                req['상위요구사항내용'] = parent_content
                updated_count += 1
        
        # 3-3. 상위요구사항내용이 없으면 빈 값으로 초기화
        if '상위요구사항내용' not in req:
            req['상위요구사항내용'] = ''
    
    # 4. 결과 저장
    print(f"\n[INFO] 파일 저장 중: {output_file}")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[ERROR] 파일 저장 실패: {e}")
        return False
    
    # 5. 결과 출력
    print(f"\n[SUCCESS] 완료!")
    print(f"   - 필드명 변경: {field_renamed_count}개")
    print(f"   - 상위 요구사항내용 자동 채움: {updated_count}개")
    print(f"   - 총 요구사항: {len(data)}개")
    
    return True

if __name__ == '__main__':
    input_file = 'v1.5_RFP_요구사항_2025-10-15.json'
    output_file = 'v1.5_RFP_요구사항_2025-10-15.json'  # 같은 파일로 덮어쓰기
    
    print("=" * 60)
    print("  상위기능명 → 상위요구사항내용 변환 스크립트")
    print("=" * 60)
    print()
    
    success = update_json_file(input_file, output_file)
    
    if success:
        print("\n[DONE] 성공적으로 완료되었습니다!")
        sys.exit(0)
    else:
        print("\n[FAILED] 실패했습니다.")
        sys.exit(1)

