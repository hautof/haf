pipeline {
  agent any
  stages {
    stage('setup') {
      steps {
        sh 'pip3 uninstall haf -y'
        sh 'python3 setup.py install'
      }
    }

    stage('test') {
      steps {
        sh 'git clone https://github.com/hautof/haf-sample'
        dir("haf-sample"){
            sh 'python3 -m haf run -c=config.json'
        }
      }
    }

    stage('teardown') {
      steps {
        sh 'pip3 uninstall haf -y'
      }
    }

  }
}