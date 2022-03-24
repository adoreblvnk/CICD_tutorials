# Jenkins tutorial

## Content

Jenkins allows developers to <mark>continuously</mark> build, test, & deploy the code to check that the application is stable. This allows for continuous development.

**Why Use Jenkinsfile?**

Instead of creating new jobs for Jenkins via GUI, Jenkinsfile is a pipeline as a code. A pipeline is a process of deploying source code from repo to production.

### Practical: Create Jenkinsfile

The [demo app](../docker%20tutorial/README.md) from Docker tutorial will be used. All code files wil be located there.

### Jenkinsfile Syntax

```groovy
pipeline {
    agent any

    // Environmental Variables
    environment {
        NEW_VERSION = "1.3.0"
        SERVER_CREDENTIALS = credentials("server_credentials")
    }

    // Tools
    tools {
        go "go1.15.7"
    }

    // Parameters
    parameters {
        string(name: "VERSION", defaultValue: "", description: "version to deploy on production")
        choice(name: "VERSION", choices: ["1.1.0", "1.2.0", "1.3.0"], description: "you mom")
        booleanParam(name: "executeTest", defaultValue: true, description: "")
    }

    stages {
        stage("build") {

            // Conditionals
            when {
                expression {
                    BRANCH_NAME == "dev" || BRANCH_NAME == "master"
                }
            }

            steps {
                echo "building application version ${NEW_VERSION} . . ."
            }
        }
        stage("test") {

            // Parameters
            when {
                expression {
                    params.executeTest
                }
            }

            steps {

                // Groovy Script
                script {
                    def youMom = "/path/to/you/mom"
                    if (youMom) {
                        println "youMom exists"
                        echo "testing application version ${VERSION} . . ."
                    }
                }

            }
        }
        stage("deploy") {
            steps {
                echo "deploying the application . . ."

                // Credentials with Wrappers
                withCredentials([
                    usernamePassword(credentials: "server_credentials", usernameVariable: USER, passwordVariable: PWD)
                ]) {
                    sh "script ${USER} ${PWD}"
                }

            }
        }
    }
    post {
        always {
            // always executed despite end result
        }
        success {
            // only executed if all stages pass
        }
        failure {
            // only executed if any stage fails
        }
    }
}
```

**Required**

- **pipeline**: For declarative Jenkins pipelines (ie 99% of Jenkinsfiles).
- **agent**: Where to execute (eg `agent any` means it'll be executed on any Jenkins node / executor). Useful to specify when there are Jenkins master & slave nodes in cluster.
- **stages**: Where the "work" actually happens (eg `build`, `test`, `deploy`). All scripts go inside them.

**Optional**

- **post**: Executes after <mark>all stages are executed</mark>.

### Conditionals

The `when { expression {} }` statement is like an `if` statement. When the condition is true, the following steps are executed. See [Environmental Variables](#environmental-variables) for example.

### Environmental Variables

Env vars can be called by `<env_var>` or `env.<env_var>`. Jenkins default env vars are listed [here](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#using-environment-variables).

**Example**

```groovy
// Conditionals
when {
    expression {
        BRANCH_NAME == "dev" || BRANCH_NAME == "master"
    }
}
```

The following code translate to: if BRANCH_NAME is dev or master, the expression is true.

**Custom Environmental Variables**

Create custom env vars with `environment`. Use custom env vars with `${<env_var>}`.

**Using Jenkins Credentials**

Sometimes you want to use credentials defined in Jenkins GUI, but in Jenkinsfile. Enable this by enabling "Credentials Binding" & "Credentials" plugins from Jenkins GUI.

Access the specific credential with `credential("<credential_ID>)`. Credential ID is defined when adding credentials in Jenkins GUI.

**Example**

```groovy
// Environmental Variables
environment {
    NEW_VERSION = "1.3.0"
    SERVER_CREDENTIALS = credentials("server_credentials")
}
```

**Defining Credentials by using Wrappers**

If credentials are not desired to be stored as env vars, it can be declared by using wrappers. Use `withCredentials()` to bind credentials to variables. The function takes in an object as a parameter (defined with `[]`). The object is the function for the type of credential (eg the function `usernamePassword()` is defined in Jenkins GUI when creating credentials).

`usernamePassword()` takes 3 parameters: `<credential_ID>`, `<username>`, & `<password>`. They are not strictly named, but are strictly ordered.

**Example 2**

```groovy
// Credentials with Wrappers
withCredentials([
    usernamePassword(credentials: "server_credentials", usernameVariable: USER, passwordVariable: PWD)
]) {
    sh "script ${USER} ${PWD}"
}
```

### Build Tools

To use build tools, add `tools`. The tools will be installed & added into `$PATH`. The name of the tool can be found in "Global Tool Configuration" in Jenkins GUI. Execute tools using `sh` command.

For tools not listed in the default Jenkins configuration, install from "Manage Plugins", then restart Jenkins.

**Example**

```groovy
// Tools
tools {
    go "go1.15.7"
}
```

### Parameters

To change Jenkins behaviour after it starts, use `parameters` for user to modify configuration. Parameters are available as `string`, `booleanParam`, `choice`, & others. For each parameter, a `name`, `defaultValue`, & `description` are necessary keys. Parameters can be used by `params.<parameter_name>`.

In Jenkins GUI, "Build" is replaced with "Build with Parameters".

**Example**

```groovy
// Parameters
parameters {
    string(name: "VERSION", defaultValue: "", description: "version to deploy on production")
    choice(name: "VERSION", choices: ["1.1.0", "1.2.0", "1.3.0"], description: "you mom")
    booleanParam(name: "executeTest", defaultValue: true, description: "")
}
. . .
// Parameters
when {
    expression {
        params.executeTest
    }
}
```

_NOTE: `params.executeTest` is the same as `params.executeTest == true`._

### Groovy Script

Jenkinsfile offers basic logic. To enhance this, we can use Groovy scripts to do more (eg define variables, if else statements, try catch statements). These are enclosed in `script` tags.

```groovy
// Groovy Script
script {
    def youMom = "/path/to/you/mom"
    if (youMom) {
        println "youMom exists"
        echo "testing application version ${VERSION} . . ."
    }
}
```

### Tips

1. Modify Jenkinsfile in Jenkins GUI
   - Navigate into the branch, then "Replay".
   - This is useful for debugging or for short term changes.

## Credits
