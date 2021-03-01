echo "Make sure you are logged in as kubeadmin"

ODS_OPERATOR_PROJECT=${ODS_OPERATOR_NAMESPACE:-"redhat-ods-operator"}

oc new-project $ODS_OPERATOR_PROJECT
oc create -f service_account.yaml
oc create -f role.yaml
oc create -f cluster_role_binding.yaml
oc create -f kfdef.apps.kubeflow.org_kfdefs_crd.yaml
oc create -f operator.yaml
