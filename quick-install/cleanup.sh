ODS_OPERATOR_PROJECT=${ODS_OPERATOR_NAMESPACE:-"redhat-ods-operator"}
ODS_PROJECT=${ODS_CR_NAMESPACE:-"redhat-ods-applications"}
ODS_MONITORING_PROJECT=${ODS_MONITORING_NAMESPACE:-"redhat-ods-monitoring"}

oc delete -f operator.yaml -n $ODS_OPERATOR_PROJECT 
oc delete kfdef opendatahub -n $ODS_PROJECT --force --grace-period=0 &
oc patch -n $ODS_PROJECT kfdef opendatahub --type=merge -p '{"metadata": {"finalizers":null}}'
oc delete -f cluster_role_binding.yaml -n $ODS_OPERATOR_PROJECT
oc delete -f role.yaml -n $ODS_OPERATOR_PROJECT
oc delete -f service_account.yaml -n $ODS_OPERATOR_PROJECT
oc delete project $ODS_PROJECT --force --grace-period=0
oc delete project $ODS_OPERATOR_PROJECT --force --grace-period=0
oc delete crd kfdefs.kfdef.apps.kubeflow.org
oc delete project $ODS_MONITORING_PROJECT --force --grace-period=0
