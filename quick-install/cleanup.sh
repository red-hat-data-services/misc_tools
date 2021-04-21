#! /bin/bash

oc delete -f catalogsource.yaml
oc delete -f fakesecret.yaml
oc delete kfdef opendatahub -n redhat-ods-applications --force --grace-period=0 &
oc patch -n redhat-ods-applications kfdef opendatahub --type=merge -p '{"metadata": {"finalizers":null}}'
oc delete crd kfdefs.kfdef.apps.kubeflow.org
oc delete project redhat-ods-operator --force --grace-period=0
oc delete clusterrolebinding prometheus-scraper
oc delete clusterrole prometheus-scraper
oc delete rolebinding cluster-monitor-rhods-reader -n redhat-ods-monitoring
oc delete service alertmanager -n redhat-ods-monitoring
oc delete service prometheus -n redhat-ods-monitoring
oc delete configmap prometheus -n redhat-ods-monitoring
oc delete configmap alertmanager -n redhat-ods-monitoring
oc delete secret grafana-config -n redhat-ods-monitoring
oc delete secret grafana-proxy-config -n redhat-ods-monitoring
oc delete secret grafana-datasources -n redhat-ods-monitoring
oc delete clusterrolebinding prometheus-scraper
oc delete clusterrolebinding grafana-auth-rb
oc delete clusterrolebinding grafana
oc delete clusterrole prometheus-scraper
oc delete project redhat-ods-applications --force --grace-period=0
oc delete project redhat-ods-monitoring --force --grace-period=0
