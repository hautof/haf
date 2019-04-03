pipeline {
  agent any
  stages {
    stage('setup') {
      steps {
        sh "ls"
      }
    }

    stage('test') {
      steps {
        checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: 'haf-sample']], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/hautof/haf-sample']]])
        sh 'cp -rf ./haf-sample/* ./'
        sh 'python3 -m haf run -c=config.json'
        sh 'rm -rf .coverage.*'
        sh 'coverage run --parallel-mod --source=./haf/ -m haf run -c=config.json'
        sh 'coverage combine'
        sh 'coverage report'
      }
    }

    stage('teardown') {
      steps {
        sh 'pip3 install haf -U'
      }
    }

  }
}