#!/usr/bin/env groovy

node {
	try {
		stage('Checkout') {
			checkout scm
		}
		
		stage('Build') {
			def mvnHome = tool 'apache-maven-3.2.3'
			bat "${mvnHome}/bin/mvn clean package -Dmaven.test.skip=true"
		}
			
		stage('Deploy') {
			echo "Stage - Deploy"
		}
	} catch (err) {
		currentBuild.result = "FAILED"
		throw err
	} finally {
	
	}
}