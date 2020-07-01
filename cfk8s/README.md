# Use Budget Alerts to scale down deployment and control costs

**Motivation**: During the initial phase of development of your application you need to have absolute control of the costs associated to your Kubernetes Cluster. GCP has [budget and budget alerts](https://cloud.google.com/billing/docs/how-to/budgets) so you can have absolute control of what you spend.

**Steps**

1. Follow the [relevant section of the documentation](https://cloud.google.com/billing/docs/how-to/budgets#create-budget) to create a budget.
2. [Create a Pub/Sub topic and create programmatic notifications](https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#manage-notifications) for the budget created on step 1. From now, the name of the Pub/Sub topic will be referred to as `[PUB-SUB-BUDGET-TOPIC]`.
3. Follow the [Quickstart to create your first GKE Cluster](https://cloud.google.com/kubernetes-engine/docs/quickstart) (notice that the code on the main.py function is based on this deployment, but it can be changed very easily according to your needs).
4. Make sure that both your [Compute Engine Default Service Account](https://cloud.google.com/compute/docs/access/service-accounts#default_service_account) and [App Engine Default Service Account](https://cloud.google.com/appengine/docs/standard/python3/service-account) have their default permissions (which by default should have the Editor role assigned).
5. Clone the repository in your local PC and go to the folder where the main.py and requirements.txt are located.
6. Change the following variables on the main.py file according to the specifics for your project:

```
...
    project_id = "[PROJECT-ID]"
    zone = "[ZONE]"
    cluster_id = "[CLUSTER-NAME]"
...
```

7. Launch the Cloud Function with the following command:

```
gcloud functions deploy [CLOUD-FUNCTION-NAME e.g. k8sbudget] --trigger-topic [PUB-SUB-BUDGET-TOPIC e.g. examplek8s] --runtime python37 --entry-point test_gke --timeout 540s
```
