from google.auth import compute_engine
from google.cloud.container_v1 import ClusterManagerClient
from kubernetes import client
from kubernetes.client.rest import ApiException

def update_deployment(api_instance, deployment):
    #Downscale the deployment to zero replicas
    deployment.spec.replicas = 0
    # Update the deployment
    try:
        api_response = api_instance.patch_namespaced_deployment(
            name=deployment.metadata.name,
            namespace=deployment.metadata.namespace,
            body=deployment)
            print("Deployment updated. status='%s'" % str(api_response.status))
    except ApiException as e:
        print("Exception when calling AppsV1Api->patch_namespaced_deployment: %s\n" % e)

def test_gke(data, context):
    project_id = "[PROJECT-ID]"
    zone = "[ZONE]"
    cluster_id = "[CLUSTER-NAME]"

    credentials = compute_engine.Credentials()

    cluster_manager_client = ClusterManagerClient(credentials=credentials)
    cluster = cluster_manager_client.get_cluster(project_id, zone, cluster_id)

    configuration = client.Configuration()
    configuration.host = f"https://{cluster.endpoint}:443"
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + credentials.token}
    client.Configuration.set_default(configuration)

    v1 = client.AppsV1Api()

    #Try to list all the deployments.
    try:
        deployments = v1.list_deployment_for_all_namespaces()
    except ApiException as e:
        print("Exception when calling AppsV1Api->list_deployment_for_all_namespaces: %s\n" % e)
    
    #Loop through the deployments to find the specfic hello-server deployment and update accordingly.
    for deployment in deployments.items:
        if 'hello' in deployment.metadata.name:
                print("%s\t%s" % (deployment.metadata.namespace, deployment.metadata.name))
                update_deployment(v1,deployment)
    return("Ok")
