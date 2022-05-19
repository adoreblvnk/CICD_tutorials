# Kubectl Commands

Useful `kubectl` commands. Concise version of [kubectl-commands](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands) To be updated.

## K8s Resource Shortnames

|         Resource          | Shortname |
| :-----------------------: | :-------: |
|         ConfigMap         |    cm     |
|         Namespace         |    ns     |
|           Nodes           |    no     |
|     PersistentVolume      |    pv     |
|   PersistentVolumeClaim   |    pvc    |
|            Pod            |    po     |
|          Service          |    svc    |
| CustomResourceDefinitions |    crd    |
|        Deployments        |  deploy   |
|        ReplicaSets        |    rs     |
|       StatefulSets        |    sts    |
|         CronJobs          |    cj     |
|      NetworkPolicies      |  netpol   |

## Tips

1. `alias k=kubectl`: Alias for `kubectl`.
2. `alias kc='k config view --minify | grep name'`: List all configured contexts & namespaces.

## Credits

- blvnk
