
from typing import List, Dict, Union

class Recommender:
    @staticmethod
    def recommend_spark_jobs(jobs: List[Dict]) -> List[Dict]:
        recommendations = []
        for job in jobs:
            cpu_over = job["executor_cores"] * 0.8 < job["avg_cpu_usage"]
            mem_over = float(job["executor_memory"].strip("GB")) * 0.8 < job["avg_cpu_usage"]

            if cpu_over or mem_over:
                recommendations.append({
                    "job_id": job["job_id"],
                    "type": "Spark",
                    "action": "Right-size executors",
                    "confidence": "High",
                    "impact": "Medium",
                    "details": f"Current Cores: {job['executor_cores']}, Avg Usage: {job['avg_cpu_usage']}"
                })
        return recommendations

    @staticmethod
    def recommend_k8s_workloads(pods: List[Dict]) -> List[Dict]:
        recommendations = []
        for pod in pods:
            try:
                # Helper function to convert memory strings to GiB
                def parse_memory(mem_str):
                    mem_str = mem_str.strip()
                    if mem_str.endswith("Mi"):
                        return float(mem_str[:-2]) / 1024  # Convert MiB to GiB
                    elif mem_str.endswith("Gi"):
                        return float(mem_str[:-2])
                    else:
                        return float(mem_str)  # Assume bytes or parse accordingly if needed

                # Parse CPU and memory
                cpu_req = int(pod["cpu_request"].strip("m"))  # millicores
                mem_req = parse_memory(pod["memory_request"])
                cpu_used = int(pod["avg_cpu_usage"].strip("m"))
                mem_used = parse_memory(pod["avg_memory_usage"])

                # Check over-provisioning
                if cpu_req > cpu_used * 2 or mem_req > mem_used * 2:
                    recommendations.append({
                        "pod_name": pod["pod_name"],
                        "type": "Kubernetes",
                        "action": "Reduce CPU/Memory request",
                        "confidence": "High",
                        "impact": "High",
                        "details": f"Request: {pod['cpu_request']}/{pod['memory_request']}, Used: {pod['avg_cpu_usage']}/{pod['avg_memory_usage']}"
                    })
            except Exception as e:
                print(f"Error processing pod {pod.get('pod_name', 'unknown')}: {e}")
        return recommendations

    @staticmethod
    def recommend_cloud_services(resources: List[Dict]) -> List[Dict]:
        recommendations = []
        for res in resources:
            if "vm_id" in res:
                try:
                    cpu_util = res["cpu_utilization_avg"]
                    days_inactive = res["days_inactive"]
                    vm_id = res["vm_id"]

                    if cpu_util < 5 and days_inactive > 7:
                        recommendations.append({
                            "resource_id": vm_id,
                            "type": "Cloud_VM",
                            "category": "VM",
                            "action": "Consider shutdown or rightsizing",
                            "confidence": "High",
                            "impact": "High",
                            "details": f"CPU Util: {cpu_util}%, Inactive Days: {days_inactive}"
                        })
                except KeyError as e:
                    print(f"Missing expected key in VM data: {e}")

            elif "storage_id" in res:
                try:
                    last_accessed = res["last_accessed_days_ago"]
                    storage_type = res["storage_type"]
                    storage_id = res["storage_id"]
                    total_size_gb = res["total_size_gb"]

                    if last_accessed > 90:
                        action = "Archive or delete unused storage"
                        confidence = "Medium" if last_accessed < 365 else "High"
                        impact = "Medium" if last_accessed < 365 else "High"

                        recommendations.append({
                            "resource_id": storage_id,
                            "type": "Cloud_Storage",
                            "category": "Storage",
                            "action": action,
                            "confidence": confidence,
                            "impact": impact,
                            "details": f"Type: {storage_type}, Size: {total_size_gb}GB, Last Accessed: {last_accessed} days ago"
                        })
                except KeyError as e:
                    print(f"Missing expected key in Storage data: {e}")

            elif "network_id" in res:
                try:
                    traffic_tb = res["egress_traffic_tb"]
                    monthly_cost = res["monthly_cost"]
                    region = res["region"]

                    if monthly_cost > 300:
                        recommendations.append({
                            "resource_id": res["network_id"],
                            "type": "Cloud_Network",
                            "category": "Network",
                            "action": "Optimize egress traffic",
                            "confidence": "High",
                            "impact": "High",
                            "details": f"Region: {region}, Egress: {traffic_tb}TB, Monthly Cost: ${monthly_cost}"
                        })
                except KeyError as e:
                    print(f"Missing expected key in Network data: {e}")
        return recommendations

    @staticmethod
    def recommend_databases(dbs: List[Dict]) -> List[Dict]:
        recommendations = []
        for db in dbs:
            if db["cpu_utilization"] < 10 and db["active_connections"] < 5:
                recommendations.append({
                    "db_instance": db["db_instance"],
                    "type": "Database",
                    "action": "Downscale instance",
                    "confidence": "Medium",
                    "impact": "Medium",
                    "details": f"CPU Util: {db['cpu_utilization']}%, Active Connections: {db['active_connections']}"
                })
        return recommendations

    def generate_recommendations(self, spark_data, k8s_data, cloud_data, db_data):
        return (
            self.recommend_spark_jobs(spark_data) +
            self.recommend_k8s_workloads(k8s_data) +
            self.recommend_cloud_services(cloud_data) +
            self.recommend_databases(db_data)
        )