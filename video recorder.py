import cv2
import numpy as np

# 카메라 캡처
cap = cv2.VideoCapture(0)

# 비디오 저장을 위한 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 20.0
frame_width = int(cap.get(3))  # 가로 해상도
frame_height = int(cap.get(4))  # 세로 해상도

# 필터 모드 초기값 설정
filter_mode = 'None'

# Record 모드 상태
is_recording = False
out = None  # 비디오 저장 객체

# 필터 모드 설정과 영상 캡처
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 필터에 따른 처리
    if filter_mode == 'Brightness/Contrast':
        alpha = 1.5  # 대비
        beta = 30     # 밝기
        filtered_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    
    elif filter_mode == 'Grayscale':
        filtered_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 그레이스케일을 3채널로 변환
        filtered_frame = cv2.cvtColor(filtered_frame, cv2.COLOR_GRAY2BGR)
    
    elif filter_mode == 'Blur':
        filtered_frame = cv2.GaussianBlur(frame, (15, 15), 0)
    
    else:
        filtered_frame = frame  # 필터 모드가 없으면 원본 프레임 그대로

    # 화면에 필터된 영상 표시
    cv2.imshow(f'Video with {filter_mode} Filter', filtered_frame)

    # Record 모드일 때 영상 저장
    if is_recording:
        if out is None:
            out = cv2.VideoWriter('output_with_filters.avi', fourcc, fps, (frame_width, frame_height))
        out.write(filtered_frame)  # 비디오 파일로 저장

    # 키 입력에 따른 동작
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC 키 - 종료
        print("ESC key pressed. Exiting...")
        break

    elif key == ord('f'):  # F 키 - 필터 모드 변경
        print("F key pressed. Changing filter...")
        if filter_mode == 'None':
            filter_mode = 'Brightness/Contrast'
        elif filter_mode == 'Brightness/Contrast':
            filter_mode = 'Grayscale'
        elif filter_mode == 'Grayscale':
            filter_mode = 'Blur'
        elif filter_mode == 'Blur':
            filter_mode = 'None'

    elif key == ord(' '):  # Space 키 - Record/Preview 모드 전환
        print("Space key pressed. Toggling record/preview mode...")
        is_recording = not is_recording
        if is_recording:
            print("Recording started...")
        else:
            print("Recording stopped...")
            if out:
                out.release()  # 비디오 파일 저장 종료
                out = None  # 객체 초기화
# 리소스 해제

cap.release()
if out:
    out.release()  # 비디오 객체 해제
cv2.destroyAllWindows()
