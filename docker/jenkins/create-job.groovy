import jenkins.model.*
import hudson.model.*

def jobName = "xumes"
def jenkins = Jenkins.instance
def xmlConfig = """
<flow-definition plugin="workflow-job@2.40">
  <actions/>
  <description/>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>PROJECT_NAME</name>
          <defaultValue>flappy_bird</defaultValue>
          <description>Project name in xumes_examples</description>
        </hudson.model.StringParameterDefinition>
        <hudson.model.StringParameterDefinition>
          <name>BRANCH_NAME</name>
          <defaultValue>flappy-bird</defaultValue>
          <description>Branch name to check out</description>
        </hudson.model.StringParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.92">
    <script>pipeline {
    agent any

    parameters {
        string(name: 'PROJECT_NAME', defaultValue: 'flappy_bird', description: 'Project name in xumes_examples')
        string(name: 'BRANCH_NAME', defaultValue: 'flappy-bird', description: 'Branch name to check out')
    }

    stages {
        stage('Clone repository') {
            steps {
                checkout([
                    \$class: 'GitSCM',
                    branches: [[name: "\${params.BRANCH_NAME}"]],
                    userRemoteConfigs: [[
                        url: 'https://github.com/mastainvin/Xumes-Examples.git',
                    ]],
                    extensions: [[\$class: 'RelativeTargetDirectory', relativeTargetDir: "xumes_examples"]]
                ])
            }
        }

        stage('Test') {
            steps {
                script {
                    sh \"\"\"
                        /home/jenkins/godot-fork/bin/godot.linuxbsd.editor.x86_64.llvm --editor --path /var/jenkins_home/workspace/xumes/xumes_examples/Godot/\${params.PROJECT_NAME} --headless &gt; godot_output.log 2&gt;&amp;1 &amp;

                        wait_for_port() {
                          while ! nc -z localhost 8080; do
                            sleep 1
                          done
                        }

                        wait_for_port

                        cd /var/jenkins_home/workspace/xumes/xumes_examples/Godot/\${params.PROJECT_NAME}
                        /home/jenkins/xumes_env/bin/python -m xumes test ./Tests/PipeSizeTest/features/ -i 20 --info -h 10
                    \"\"\"

                    junit "**/test-results.xml"
                }

            }

        }
    }
}</script>
    <sandbox>true</sandbox>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
"""

if (jenkins.getItem(jobName) == null) {
    def xmlStream = new ByteArrayInputStream(xmlConfig.getBytes())
    jenkins.createProjectFromXML(jobName, xmlStream)
    println "Job '${jobName}' created successfully."
} else {
    println "Job '${jobName}' already exists. Skipping creation."
}
