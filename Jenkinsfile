pipeline{
    agent {label 'build-vm'}
    environment{
        IMAGE = "jyotimanab/ecommerce-product-service"
        TAG = "${env.BUILD_NUMBER}"
    }
    stages{
        stage('git checkout'){
            steps{
                git(url: 'https://github.com/zerotoprodevops/ecommerce-product-service.git', branch: 'main')
            }

        }
        stage('Build Stage'){
            steps{
                sh "docker build -t $IMAGE:$TAG ."
            }
        }
        stage('Scan with Trivy'){
            steps{
                sh "TMPDIR=/tempdir trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 $IMAGE:$TAG"
            }
        }
    }
}