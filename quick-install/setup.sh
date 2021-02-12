echo "Make sure you are logged in as kubeadmin"

oc new-project redhat-rhods
oc create -f service_account.yaml
oc create -f role.yaml
oc create -f cluster_role_binding.yaml
oc create -f kfdef.apps.kubeflow.org_kfdefs_crd.yaml
oc create -f operator.yaml
