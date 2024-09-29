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
        <hudson.model.ChoiceParameterDefinition>
          <name>Game</name>
          <description>The game you want to test.</description>
          <choices class="java.util.Arrays\$ArrayList">
            <a class="string-array">
              <string>flappy_bird</string>
              <string>smb</string>
              <string>smb_jump_change</string>
            </a>
          </choices>
        </hudson.model.ChoiceParameterDefinition>
        <hudson.model.StringParameterDefinition>
          <name>Tries</name>
          <description>Number of test iterations</description>
          <defaultValue>20</defaultValue>
          <trim>false</trim>
        </hudson.model.StringParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.92">
    <script>

    pipeline {
        agent any

        parameters {
            choice(name: "Game", choices: ['flappy_bird', 'smb', 'smb_jump_change','tanks-of-freedom-ii'], description: 'The game you want to test.')
            string(name: "Tries", defaultValue: '20')
        }

        stages {
            stage('Clone repository') {
                steps {
                    checkout([
                        \$class: 'GitSCM',
                        branches: [[name: "main"]],
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
                              /home/jenkins/godot-source/bin/godot.linuxbsd.editor.x86_64.llvm --editor --path \${env.WORKSPACE}/xumes_examples/Godot/\${params.Game} --headless > godot_output.log 2&gt;&amp;1 &amp;

                            wait_for_port() {
                              while ! nc -z localhost 8080; do
                                sleep 1
                              done
                            }

                            wait_for_port
                        \"\"\"

                        def features_path = ""
                        def options = ""
                        if (params.Game == "flappy_bird") {
                            features_path = "./Tests/PipeSizeTest/features/"
                        } else if (params.Game == "smb" || params.Game == "smb_jump_change"){
                            features_path = "./tests/features/"
                        } else if (params.Game == "tanks-of-freedom-ii") {
                            features_path = "./tests/features/"
                            options = "-nv"

                        }

                        int tries = params.Tries as Integer

                        sh \"\"\"
                            cd \${env.WORKSPACE}/xumes_examples/Godot/\${params.Game}
                            /home/jenkins/xumes_env/bin/python -m xumes test \${features_path} -i \${tries} --info -h 10 \${options}
                        \"\"\"
                        junit "**/test-results.xml"

                    }

                }

            }
        }
}

</script>
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
