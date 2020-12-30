# ❓ 문제 인식 (Problem Definition)

2020년 2월, 코로나 19가 급격히 확산되면서 코로나 19 이후의 뉴노멀과 함께 ‘언택트 사회’ 라는 새로운 변화가 소매, 유통, 원격 학습 등의 분야로 빠르게 확산됨. <br>

동시에 직원과 직접 마주치는 것을 원치 않는 2030 세대의 소비 성향과 유통사의 인건비 절감 요구가 맞아떨어진 결과, 점차 확장되어온 언택트 소비 패턴. <br>

사람 · 현금 없이 운영되는 언택트 매장이 코로나 19 영향으로 더욱 주목받고 있음. <br>

코로나 19 여파로 집콕 수요가 늘어남에 따라 올해 3분기 온라인 쇼핑 거래액이 통계 이래 최고 금액 수준을 기록했다는 연구 결과. <br>

동시에 안전한 환경에서 직접 물건을 맨눈으로 직접 확인한 후에 구매하려는 소비자들의 수요 증가. <br>

이에 무인 상점 시스템과 더불어 ‘얼굴 인식 기반 체크인/체크아웃 시스템’을 구현하여 문제 해결에 도전해보고자 함.  <br><br><br>

In February 2020, with the rapid spread of Covid-19, a new form of society called ‘Contact-free society’, has penatrated almost every fields such as retail, distribution, or remote learning.<br>

So-called generation 2030 has shown unique consumption pattern. <br>

From before the pendemic, many people in this group has been reluctant to shop while directly meeting other individuals. <br>

This tendency plus the demand for labor cost reduction of distributors have accelerated the expansion of the 'contact-free consumption pattern'. <br>

In such background, the concept of 'contact-free stores' that automatically operates has been in the spotlight. <br> 

According to data provided by NSO(National Statistical Office) in South Korea, as the effect of pendamic, online shopping transactions in the third quarter of 2020 have reached the highest level since ever been counted.<br>

At the same time, increasing demand from consumers who want to purchase products after checking them with the naked eye in a safe environment.<br> 

Therefore, we will try to solve the problem by implementing a “face recognition-based check-in/check-out system” along with the unmanned store system.<br>


# 🏃 산업 동향 (Industrial Trends)
최근 인공지능 기술을 이용한 얼굴 인식의 정확도가 높아짐에 따라 범죄, 보안, 유통, 금융 등 다양한 분야에서 적용 사례 증가.<br>
특히 생체인식 기술 중에서 얼굴 인식은 인식 장비와 접촉하지 않아 위생적이고 편의성이 높아 다양한 분야에서의 활용성이 기대됨.<br>
글로벌 얼굴인식 시장은 연평균 22%의 성장률을 보여 성장 전망도 매우 긍정적.<br>

# 👨🏻‍🔬 개발 필요성 (Research Background)
컴퓨터 비전과 딥러닝 기반의 무인화 상점 플랫폼 개발을 통해 기존에 대면으로 이루어지던 소비 패턴을 간편하고 빠른 자동화 시스템으로 대체.<br>
데이터베이스와의 연동을 통해 고객의 결제 방법과 정보 자동 매핑,<br>
실시간으로 가상 장바구니에 담긴 상품들을 앱으로 확인,<br>
대면으로 실행되던 결제 단계 생략으로 사람 간의 접촉을 줄이고 시간 단축.<br>
다양한 센서와 다량의 카메라를 사용하는 아마존고의 기술을 오직 카메라 한 대와 최신 컴퓨터 비전 알고리즘만으로 단기간 내 구현 및 최적화에 도전.<br>

# 📝 레퍼런스 (Reference)
* <b> GitHub </b><br>
Yolov4 https://github.com/Tianxiaomo/pytorch-YOLOv4 <br>
Yolov5 https://github.com/ultralytics/yolov5 <br>
DeepSort https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch <br>
OpenPose https://github.com/CMU-Perceptual-Computing-Lab/openpose.git <br>
Darknet https://github.com/pjreddie/darknet.git <br>
LabelImg https://github.com/tzutalin/labelImg <br>
FaceRecognition https://github.com/ageitgey/face_recognition <br>
FaceNet https://github.com/timesler/facenet-pytorch <br>
* <b>Official Papers</b> <br>
Yolov4 https://arxiv.org/pdf/2004.10934.pdf <br>
Yolov5  -  On the way! <br>
FaceRecognition https://arxiv.org/pdf/1804.06655.pdf <br>
FaceNet https://arxiv.org/pdf/1503.03832.pdf <br>
Face Augmentation https://arxiv.org/pdf/1904.11685.pdf
