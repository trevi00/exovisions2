# Kubernetes Deployment Manifests

Kubernetes 배포를 위한 매니페스트 파일들입니다.

## 파일 구조

```
k8s/
├── namespace.yaml              # exoplanet 네임스페이스
├── configmap.yaml              # 환경 변수 설정
├── secrets.yaml                # 민감 정보 (DB 비밀번호 등)
├── database-statefulset.yaml  # PostgreSQL StatefulSet
├── backend-deployment.yaml    # Backend Deployment + Service
├── frontend-deployment.yaml   # Frontend Deployment + Service
└── ingress.yaml                # Nginx Ingress
```

## 사전 준비

### 1. Kubernetes 클러스터

- Kubernetes 1.24+
- kubectl 설치 및 설정 완료
- Nginx Ingress Controller 설치

### 2. Nginx Ingress Controller 설치

```bash
# Helm으로 설치 (권장)
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace

# 또는 kubectl로 설치
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.9.5/deploy/static/provider/cloud/deploy.yaml
```

### 3. Secret 설정

```bash
# Base64 인코딩된 실제 값으로 secrets.yaml 수정
echo -n "your-db-password" | base64
# 출력된 값을 secrets.yaml에 업데이트
```

## 배포 방법

### Option 1: kubectl로 직접 배포

```bash
# 순서대로 배포
kubectl apply -f namespace.yaml
kubectl apply -f secrets.yaml
kubectl apply -f configmap.yaml
kubectl apply -f database-statefulset.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f ingress.yaml

# 배포 확인
kubectl get all -n exoplanet
kubectl get ingress -n exoplanet
```

### Option 2: ArgoCD로 배포 (권장)

ArgoCD를 사용한 GitOps 배포는 `argocd/README.md` 참조

## 설정 변경

### Image 태그 업데이트

```bash
# backend-deployment.yaml 수정
sed -i 's|image: ghcr.io/.*/backend:.*|image: ghcr.io/YOUR_USERNAME/exovisions2/backend:v1.2.3|g' backend-deployment.yaml

# frontend-deployment.yaml 수정
sed -i 's|image: ghcr.io/.*/frontend:.*|image: ghcr.io/YOUR_USERNAME/exovisions2/frontend:v1.2.3|g' frontend-deployment.yaml

# 적용
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
```

### Replicas 변경

```bash
# Backend replicas 변경
kubectl scale deployment backend -n exoplanet --replicas=3

# 또는 파일 수정 후 적용
kubectl apply -f backend-deployment.yaml
```

### 환경 변수 변경

```bash
# ConfigMap 수정
kubectl edit configmap exoplanet-config -n exoplanet

# 또는 파일 수정 후 적용
kubectl apply -f configmap.yaml

# Pod 재시작 (변경사항 반영)
kubectl rollout restart deployment/backend -n exoplanet
kubectl rollout restart deployment/frontend -n exoplanet
```

## 모니터링

### Pod 상태 확인

```bash
# 모든 리소스 확인
kubectl get all -n exoplanet

# Pod 로그 확인
kubectl logs -f deployment/backend -n exoplanet
kubectl logs -f deployment/frontend -n exoplanet

# Pod describe (상세 정보)
kubectl describe pod <POD_NAME> -n exoplanet
```

### Ingress 상태 확인

```bash
# Ingress 정보
kubectl get ingress -n exoplanet
kubectl describe ingress exoplanet-ingress -n exoplanet

# External IP 확인
kubectl get svc -n ingress-nginx
```

### Metrics

```bash
# Pod 리소스 사용량
kubectl top pods -n exoplanet

# Node 리소스 사용량
kubectl top nodes
```

## 롤백

```bash
# Deployment 롤백 이력 확인
kubectl rollout history deployment/backend -n exoplanet

# 이전 버전으로 롤백
kubectl rollout undo deployment/backend -n exoplanet

# 특정 리비전으로 롤백
kubectl rollout undo deployment/backend -n exoplanet --to-revision=3
```

## 삭제

```bash
# 리소스 삭제 (데이터는 유지)
kubectl delete -f ingress.yaml
kubectl delete -f frontend-deployment.yaml
kubectl delete -f backend-deployment.yaml
kubectl delete -f database-statefulset.yaml

# 전체 네임스페이스 삭제 (모든 리소스 + 데이터 삭제)
kubectl delete namespace exoplanet
```

## 트러블슈팅

### Pod가 시작되지 않음

```bash
# Pod 상태 확인
kubectl get pods -n exoplanet

# 이벤트 확인
kubectl get events -n exoplanet --sort-by='.lastTimestamp'

# Pod 로그 확인
kubectl logs <POD_NAME> -n exoplanet

# 이전 컨테이너 로그 (재시작된 경우)
kubectl logs <POD_NAME> -n exoplanet --previous
```

### ImagePullBackOff 에러

```bash
# Secret 확인 (GHCR 인증)
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=YOUR_GITHUB_USERNAME \
  --docker-password=YOUR_GITHUB_TOKEN \
  -n exoplanet

# Deployment에 imagePullSecrets 추가
# backend-deployment.yaml에 다음 추가:
# spec:
#   template:
#     spec:
#       imagePullSecrets:
#         - name: ghcr-secret
```

### Database 연결 실패

```bash
# PostgreSQL Pod 확인
kubectl get pods -n exoplanet | grep database

# PostgreSQL 로그 확인
kubectl logs -f statefulset/database -n exoplanet

# 수동 연결 테스트
kubectl exec -it database-0 -n exoplanet -- psql -U exoplanet -d exoplanet_db
```

### Ingress가 작동하지 않음

```bash
# Ingress Controller 확인
kubectl get pods -n ingress-nginx

# Ingress 설정 확인
kubectl describe ingress exoplanet-ingress -n exoplanet

# DNS 설정 확인
kubectl get ingress -n exoplanet
# HOSTS 열에 도메인이 표시되는지 확인
```
