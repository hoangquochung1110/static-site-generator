---
title: Kubernetes core concept
date: 2022-11-29 15:00
description: Short explanation about Kubernetes core concepts
category: undefined
---

# YAML files

- input for the creation of objects such as PODs, Replicas, Deployments, Services etc. All of these follow similar structure
- contains 4 top level fields:
    * apiVersion
    * kind
    * metadata
    * spec

It’s IMPORTANT to note that under metadata, you can only specify name or labels or
anything else that kubernetes expects to be under metadata. You CANNOT add any
other property as you wish underthis. However, under labels you CAN have any kind
of key or value pairs as you see fit. So its IMPORTANT to understand what each of
these parameters expect.


# Pod

The smallest and most fundamental object in Kubernetes.

Instead of running containers directly on nodes, Kubernetes runs them inside pods.

You can think of a pod basically as a wrapper of your Kubernetes containers. A pod usually run a single container but can also have multiple containers. So you might be wondering why Kubernetes does not run containers directly instead of running pods ? Because Pods are short-lived and having containers in Pods enables easy replication - which is one of the most important features of K8s.

Pods are immutable. You can not update fields like the name of the Pod or the name of the namespace.

___

# ConfigMap

ConfigMaps is an [API object](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/) in Kubernetes to store data in key-value pairs. It's essentially a dictionary that contains configuration settings.

ConfigMaps allow you to centralize and decouple environment-specific configuration from your containers, so that your applications are easily portable. In other words, it enables you to set different configurations for the development, staging and production environments.

ConfigMap does not provide encryption, it keeps data as plain text. Therefore, we should store non-confidential like hostname, connection strings or URLs.

Pods can consume ConfigMaps as environment variables, command-line arguments, or as configuration files in a volume. Note: pod and configmaps must be in the same namespace.

In general, there're 3 ways to consume ConfigMaps:

* Mounting a ConfigMap as a data volume
* Accessing the ConfigMap remotely by pods in the same namespace
* Defining a ConfigMap separately from pods and using them for other components of the Kubernetes cluster

### **Configure Pod to use a ConfigMap**

Let's refer to [official document](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/) for detaied instructions or brief explanation at [my gist](https://gist.github.com/hoangquochung1110/57d9911ecd94b17a5fb044dbb6bf997e)

---

# Deployment

You would never create individual pods to serve your application. Because that would mean if the traffic suddenly increases, your pod will run out of resources, and you will face downtime.

Instead of it, you create a bunch of identical pods. If one of these pods goes down or the traffic increases and you need more pods, Kubernetes will bring up more pods. The deployment controller does this management of multiple similar pods when you create a Deployment object.

Now you understand why it's recommended to create a Deployment instead of Pods. The Deployment object will create and manage pods for you. So when you run `kubectl get pods`, the pods have some random string added to their names. This means these pods were created by the deployment and not us directly.

___

# Labels

Kubernetes labels are key-value pairs that can connect identifying metadata with Kubernetes objects.

### **When to use Labels**

### Group resources for queries

Apply a certain label to resources makes it easy to view them aa with a quick query.

For example, Devops team needs to quickly learn why a development environment is unavailable. If all pods for that environment include the label `dev`, this `kubectl` command can immediately find their status:

```bash
kubectl get pods -l 'environment in (dev)'
```

Without proper labeling, the DevOps team will likely to use regular `kubectl get pods` command then use `grep` to search through its output.

### Enable bulk operations

You can use labels to query a subset of resources then perform bulk operation.
Take a scenario where a team deletes all dev and staging environments each night to reduce compute expenses. Kubernetes labels make it possible to automate that activity. For example. this command deletes all objects labeled `environment: dev` or `environment: sit`:

```bash
kubectl delete deployment,services,statefulsets -l 'environment in (dev, sit)'

```

### **6 Kubernetes labeling best practices to follow**

1. Use correct syntax

    Syntax for creating a label key-value pair is in the format `<prefix>/<name>`.

    The prefix is optional and must be a valid DNS subdomain (such as "company.com"). If you aren't distributing resources outside the company, you can skip the prefix.

    The name is the arbitrary property name of the label. For example, you can use the name `environment`with label values `production`, `testing` and `development` to label environment type effectively. A name can contains 63-char long with alphanumeric, dashes, underscores and dot characters.

2. Know your label-selection options

    Can select labels by equality or set.

    Equality-based selection: `environment-dev, release=nightly` to find all resources that include both those labels.

    Set-based selections: `environment in (dev, uat)` selects resources labels with the name `environment`and values `dev` or `uat`.

3. Use Kubernetes-recommended labels

    Kubernetes offers a [list of recommended labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/#labels) for grouping application names, instances, components, etc.

4. Standardize label naming conventions across your organization

    When labels are improperly applied, automated processes may fail, and any monitoring tools you're using may provide false-positive alerts.

5.  Add required labels to pod templates

    Including labels you consider essential in pod templates enables Kubernetes controllers to create pods with the consistent states you specify. These templates are part of workload resources, like Deployments and DaemonSets. You can begin with a small list of labels in the template. For example, ones that require environment, release, and owner labels.

6. Do a lot of labeling

    The more labeling you have in place, the easier it is to find precisely what you're looking for in Kubernetes.

References: https://www.redhat.com/sysadmin/kubernetes-labels-best-practices
