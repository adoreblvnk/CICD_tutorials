# CICD tutorials

A list of tutorials for CI/CD tools for devops. Special thanks to [TechWorld with Nana](https://www.youtube.com/c/TechWorldwithNana) for these tutorial videos.

## Content

It is recommended to start with Docker, then Kubernetes.

### [Docker](docker%20tutorial/README.md) (w/ Practical)

- Learn basic Docker commands.
- Deploy MongoDB with MongoExpress frontend.
- Learn how to create & configure DockerCompose & Dockerfiles.
- Bonus: Docker tips.

### [Kubernetes](kubernetes%20tutorial/README.md) (w/ Practical)

- Learn about main K8s components.
- Learn about K8s architecture.
- Learn how to use minikube & kubectl.
- Create & configure K8s YAML files.
- Deploy MongoDB with MongoExpress frontend.
- Learn about Namespaces.
- Learn about Ingress & how to configure security.
- Use Helm, the package manager for K8s.
- Learn K8s volumes for persistent storage.
- Learn about K8s StatefulSet for stateless applications. 

### [Istio](istio%20tutorial/README.md) (w/ Practical)

- Service mesh with sidecar pattern.
- Istio features.
- Deploy [Online Boutique](https://github.com/GoogleCloudPlatform/microservices-demo) by Google Cloud Platform using kubectl.
  - Configure automated Envoy proxy injection via Istio.
- Learn about Istio addons (Grafana, Prometheus, Jaeger, Zipkin, Kiali) for monitoring & data visualization.
  - Use Kiali for deployed application.

### [GitOps](gitops%20concepts/README.md)

- GitOps Terminologies
- GitOps Advantages
- GitOps Principle

### [Jenkins](jenkins%20tutorial/README.md) (w/ Practical)

- Jenkins Concepts
- Declarative Pipeline Syntax
- Jenkinsfile Stages
- Jenkinsfile Expressions
- Environment Variables
- Build Tools
- Parameterized Build
- External Groovy Script
- Jenkins Build
- Pipeline: Nodes & Processes
- Pipeline: Build Step 
- Tips

### [ArgoCD](argocd%20tutorial/README.md) (w/ Practical)

- CD Workflow with ArgoCD
- How ArgoCD Works
- Configuring ArgoCD
- Multi-Cluster Usage
- Practical: Deploying ArgoCD in K8s cluster.

### [OPA (Open Policy Agent)](opa%20tutorial/README.md) (w/ Practical)

- OPA Introduction
- Rego Expressions
- Basic Rego Rules
- Practical: Rego Rules & OPA Evaluation

## TODO:

- add banner to README.
- reformat unit testing / add docs.
- reformat .gitignore.
- finish base OPA tutorial.
- write a tutorial for opa gatekeeper.

## Credits

- [Techworld with Nana](https://twitter.com/Njuchi_)
- [Tim Hinrichs](https://twitter.com/tlhinrichs)
- prod by blvnk.