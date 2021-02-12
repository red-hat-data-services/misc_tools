
oc delete -f operator.yaml -n redhat-rhods 
oc delete kfdef opendatahub -n opendatahub --force --grace-period=0 &
oc patch -n opendatahub kfdef opendatahub --type=merge -p '{"metadata": {"finalizers":null}}'
oc delete -f cluster_role_binding.yaml -n redhat-rhods
oc delete -f role.yaml -n redhat-rhods
oc delete -f service_account.yaml -n redhat-rhods
oc delete project opendatahub --force --grace-period=0
oc delete project redhat-rhods --force --grace-period=0
oc delete crd kfdefs.kfdef.apps.kubeflow.org
