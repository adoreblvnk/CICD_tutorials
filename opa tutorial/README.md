# OPA & Gatekeeper Tutorial

OPA (Open Policy Agent) tutorial summary. Check out the [full tutorial](https://academy.styra.com/courses/opa-rego) @[Styra Academy](https://academy.styra.com). Big ups to them.

## Intro

![](img/policy_decoupling.png))

OPA is a policy engine that allows you to define policies and enforce them. Specifically, the service enforces the decision, but OPA makes the decision. OPA runs on the same server as the application for maximum performance.

For a microservice application, it does not need to be modified to integrate with OPA. Instead, a network proxy is used.

For Kubernetes resource configurations, OPA can be integrated in:

1. **Kubernetes API Server.** Done via a webhook during admission control so all resources must pass OPA before being deployed.
2. **CICD Pipeline.** If Kubernetes resources needs to be checked into source-control.
3. **Developer Laptops.** To evaluate policies as unit tests.

**OPA Features**

- **Declarative Policy Language (Rego)**
  - 50+ built-in functions for JWTs, datetime, CIDR math etc.
  - Context-aware policies (eg Kubernetes).
- **Library (Go), Sidecar / Host-Level Daemon**
  - OPA runs on the same server. If there are 100 Kubernetes clusters, there will be 100 OPA instances.
- **Management APIs**
  - Bundle service allows OPA to receive policies.
  - Status service for receiving status from OPA.

## Rego Expressions

![](img/rego_overview.png)

### Single Values

**Values & Variables**: Rego supports String, Number, Boolean, Array, Object, null, & Set.

**Variable Assignment**: Done with `s := "Hello World"`

_NOTE: Variables are immutable. Treat them as constants. This is because Rego is a declarative language._

**Input & Data Variables**

`input` is a global variable for storing JSON object passed to OPA.

`data` is a global variable for storing external data given to OPA (eg other rules).

**(Tip) Dot Expressions**: Dot `.` (eg `obj.key`) is shorthand for `obj["key"]`.

**Undefined**

When a path is missing, result is `undefined`, not an error (ie OPA does not throw an error, but does not display the result).

- `not` turns `undefined` to `true`.
- `not` turns `false` to `true`.
- `not` turns everything else into `undefined`.

### Comparing & Constructing Values

**Equality Expressions**: `==`

**Built-In Expressions**

Below is a non-exhaustive list of built-in functions. Refer to [Policy Reference](https://www.openpolicyagent.org/docs/latest/policy-reference/) for more.

| Category                | Functions                                                      |
| ----------------------- | -------------------------------------------------------------- |
| Basic                   | `==`, `!=`, `<`, `>`, `<=`, `>=`, `+`, `-`, `*`, `/`, `%`      |
| Strings                 | `concat`, `lower`, `trim`, `replace`, regex, glob, `split`     |
| Arrays / Sets / Objects | `concat`, `slice`, `intersection`, `union`, `remove`, `filter` |
| Aggregates              | `count`, `sum`, `min`, `sort`                                  |
| Parsing                 | base64, urlquery, json, yaml                                   |
| Tokens                  | verify, decode, encode                                         |
| Time                    | `time.date`, time, `time.add_date`                             |
| Network CIDRs           | `net.cidr_contains`, `net.cidr_intersects`, `net.cidr_expand`  |

## Basic Rego Rules

### Boolean Rules & Evaluation

**Boolean Rules**

Boolean rules are IF statements that assign a variable to `true` / `false`.

```rego
# variable `allow` is assigned to `true` if the following conditions are satisfied, else false.
default allow = false
allow = true {
    . . .
}
```

`default` is an optional keyword to set default value.

*Tip: Skip `true` for a shortcut, eg `allow = true { . . . }` is equivalent to `allow = { . . . }`.*

### Rule Chaining & Non-Boolean Rules

**Logical AND & OR Rule Evaluation**

AND is achieved by chaining condition in the same rule, eg:

```rego
allow {
    condition_1
    condition_2
}
```

OR is achieved by chaining multiple rules, eg:

```rego
allow {
    condition_1
}
allow {
    condition_2
}
```

**Non-Boolean Rules**

Specify rule assignment with `=` (eg `code = 200 { not deny }`).

Values can be computed, eg:

```rego
port_number = result {
    values := split(input.request.host, ":")
    result := to_number(values[1])
}
```

Multiple values can be returned via an object, eg:

```rego
content = result {
    result := {
        "story": "Hello World",
        "author": "hi blvnk"
    }
}
```

**Policy Decisions**

A Policy Decision is the value of the variable. This is typically used for enforcing policies.

TODO: write a tutorial for opa gatekeeper.
