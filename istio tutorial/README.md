# istio tutorial

Learning Istio from [TechWorld with Nana](https://www.youtube.com/c/TechWorldwithNana)'s tutorials. Taken from [Istio Summary](https://youtu.be/16fgzklcF7Y) & [Istio Setup in Kubernetes](https://youtu.be/voAyroDb6xk).

## Content

### Intro

**Service Mesh**: It manages <mark>communication</mark> between <mark>microservices</mark>.

### Challenges of Microservice Architecture

Components of Microservice:

1. **BL** (Business Logic)
   - Needed in every microservice.
2. **COMM** (Communication Configurations)
   - Endpoint of each microservice. This enables other microservices to communicate with each other.
3. **SEC** (Security Logic)
   - Ensures secure communication within cluster.
   - Access rules to authorize between microservice communication.
4. **R** (Retry Logic)
   - Retry the connection if a microservice loses connection.
5. **MT** (Metrics & Tracing)
   - Monitor performance (eg how many requests does each microservice send / receive?, how long each request take?).

Apart from the 1st point, the rest of the components have to be added to each application, further complicating development.

### Service Mesh with Sidecar Pattern

![](assets/sidecar_pattern.png)

**Sidecar Proxy**: Extract all non-business logic from application & acts as a proxy.

**Control Plane**: Instead of manually configuring Sidecar Proxy as a yaml file, Control Plane will <mark>automatically inject these Sidecar Proxies</mark> into <mark>every Pod</mark>.

![](assets/service_mesh.png)

The Service Mesh is the network layer.

**Traffic Split**: Configure a webserver service to <mark>redirect different amounts of traffic to different services</mark>. For example, redirecting 90% of traffic to Service v2 & 10% of traffic to Service v3; this helps to catch bugs in the newer version.

**Istio Architecture**: Envoy proxy implements the Sidecare Proxy; Istio manages the Control Plane. The Control Plane comprises of configuration, discovery, & certificates.

**Istio Configuration**

- Configured with K8s YAML files using CRD (Custom Resource Definitions) (eg `kind: DestinationRule`).
  - **CRD**: Custom K8s component for 3rd party tools.
- **2 Istio CRDs**:
  1.  **Virtual Service**: Defines how to route the traffic <mark>to</mark> the specified destination.
  2.  **DestinationRule**: Configures what happens to traffic <mark>for</mark> that destination.

These config files are converted into <mark>Envoy-specific</mark> configurations. Configurations are propagated into Proxy sidecars.

### Istio Features

**Service Discovery**: Instead of statically configuring the endpoints, we can ensure that the new microservice gets registered automatically / dynamically.

**Security**: Istiod can act as a CA & generate certificates for all microservices.

**Metrics & Tracking**: Get telemetry data from Envoy proxy & can be forwarded / analyzed by monitoring server (eg Prometheus).

**Istio Ingress Gateway**: Alternative to Nginx Ingress Controller.

CRD for Istio Ingress Gateway is `kind: Gateway`.

**Istio Traffic Flow**

![](assets/istio_traffic_flow.png)

### Download Istio & Configure Istioctl

_Note: Istioctl needs a minimum of 6 CPUs & 8192 memory._

Install [Istioctl](https://istio.io/latest/docs/setup/install/istioctl/) & add it to path.

### Install Istio in Minikube Cluster

Run in default namespace. _Note: Run `kubectl get ns`._

      istioctl install

This adds `istio-system` to namespace & adds 2 Istio pods inside it (Istiod is 1 of them).

### Deploy Microservice Application

Microservice application used here is [Online Boutique](https://github.com/GoogleCloudPlatform/microservices-demo) by Google Cloud Platform.

1. Copy [kubernetes-manifests.yaml](https://github.com/GoogleCloudPlatform/microservices-demo/blob/main/release/kubernetes-manifests.yaml) into a project file.
2. Start the microservice in default namespace.
   ```
   kubectl apply -f kubernetes-manifests.yaml
   ```
   - Run the following to check if all pods have started.
     ```
     kubectl get pod
     ```

When running the above command, notice that there is only 1 container running inside a pod. Note that <mark>Envoy proxies were NOT injected</mark>!

**Configure Automatic Envoy Proxy Injection**

This can be configured via namespace labels. To view namespace labels, run the following: `kubectl get ns <namespace> --show-labels`

      kubectl get ns default --show-labels

1. Run the following command to enable automatic Envoy proxy injection:
   ```
   kubectl label namespace default istio-injection=enabled
   ```
   - `istio-injection` tells Istio to enable it.
2. Rerun the pods.
   - Delete the current deployment.
     ```
     kubectl delete -f kubernetes-manifests.yaml
     ```
   - Start the microservice.
     ```
     kubectl apply -f kubernetes-manifests.yaml
     ```
   - _Note: We do not have to modify the existing Kubernetes files. Istio auto injects Envoy proxies just by enabling the option._
3. View any pod configuration from the application.
   ```
   kubectl describe pod <pod_name>
   ```
   - _Note: There is a new `istio-init` inside `Init Containers`. This is automatically injected by Istio._

### Istio Addons for Monitoring & Data Visualization

In [Istio Features](#istio-features), Istio collects telemetry.

1. Navigate to Istio installation folder.
2. Run the following command. This installs Grafana, Jaeger, Kiali, & Prometheus.
   ```
   kubectl apply -f samples/addons
   ```
3. View the services running in Istio.
   ```
   kubectl get svc -n istio-system
   ```
   - **Grafana**: Visualization tool.
   - **Prometheus**: Monitoring tool.
   - **Jaeger**: Trace microservice requests.
   - **Zipkin**: Jaeger alternative.
   - **Kiali**: Data visualization tool (including monitoring & tracing).

### Kiali: Service Mesh Management for Istio

1. Run Kiali. This configures port forwarding for the internal service that can't be accessed externally. This means that we can run it locally on port 20001.
   ```
   kubectl port-forward svc/kiali -n istio-system 20001
   ```
2. Navigate to `localhost:20001`.
3. The `Graph` section visualizes the network of microservices. Kiali has `Traffic`, `Inbound Metrics`, & `Traces` too.

### Labels in Pods for Istio

For visualization to work, Istio <mark>requires the `app` label</mark>. This `app` label has a special meaning in Istio.

## Credits

- [Techworld with Nana](https://twitter.com/Njuchi_)
- prod by blvnk.
