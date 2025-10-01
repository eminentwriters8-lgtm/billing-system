import os
import psutil
import platform
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from django.db.models import Sum, Count, Q
from .models import Client, ServicePlan, Invoice, Payment, NetworkUsage

class SystemManager:
    def __init__(self):
        self.start_time = timezone.now()
    
    def get_system_stats(self):
        """Get comprehensive system statistics"""
        try:
            # System performance metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Database statistics
            total_clients = Client.objects.count()
            active_clients = Client.objects.filter(is_active=True).count()
            total_plans = ServicePlan.objects.count()
            pending_invoices = Invoice.objects.filter(status='pending').count()
            paid_invoices = Invoice.objects.filter(status='paid').count()
            
            # Revenue calculations - FIXED: using Sum directly
            revenue_data = Payment.objects.aggregate(total=Sum('amount'))
            total_revenue = revenue_data['total'] or 0
            
            # Recent activity
            recent_payments = Payment.objects.filter(
                payment_date__gte=timezone.now() - timedelta(days=30)
            ).count()
            
            new_clients_this_month = Client.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=30)
            ).count()
            
            # Network usage
            total_usage = NetworkUsage.objects.aggregate(
                total_download=Sum('download_bytes'),
                total_upload=Sum('upload_bytes')
            )
            
            stats = {
                # System performance
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'memory_available': memory.available,
                'memory_total': memory.total,
                'disk_usage': disk.percent,
                'disk_free': disk.free,
                'disk_total': disk.total,
                
                # Business metrics
                'total_clients': total_clients,
                'active_clients': active_clients,
                'inactive_clients': total_clients - active_clients,
                'total_plans': total_plans,
                'pending_invoices': pending_invoices,
                'paid_invoices': paid_invoices,
                'total_revenue': total_revenue,
                'recent_payments': recent_payments,
                'new_clients_this_month': new_clients_this_month,
                
                # Network metrics
                'total_download': total_usage['total_download'] or 0,
                'total_upload': total_usage['total_upload'] or 0,
                
                # System info
                'system_uptime': str(timezone.now() - self.start_time).split('.')[0],
                'server_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'platform': platform.platform(),
            }
            
            return stats
            
        except Exception as e:
            print(f"Error getting system stats: {e}")
            return {
                'error': str(e),
                'cpu_usage': 0,
                'memory_usage': 0,
                'total_clients': 0,
                'active_clients': 0,
                'total_revenue': 0,
            }
    
    def get_performance_metrics(self):
        """Get real-time performance metrics"""
        try:
            # CPU usage per core
            cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
            
            # Memory details
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            network_io = psutil.net_io_counters()
            
            metrics = {
                'cpu_cores': len(cpu_percent_per_core),
                'cpu_percent_per_core': cpu_percent_per_core,
                'memory_percent': memory.percent,
                'memory_used_gb': round(memory.used / (1024**3), 2),
                'memory_total_gb': round(memory.total / (1024**3), 2),
                'swap_used_gb': round(swap.used / (1024**3), 2),
                'swap_total_gb': round(swap.total / (1024**3), 2),
                'disk_read_mb': round(disk_io.read_bytes / (1024**2), 2) if disk_io else 0,
                'disk_write_mb': round(disk_io.write_bytes / (1024**2), 2) if disk_io else 0,
                'network_sent_mb': round(network_io.bytes_sent / (1024**2), 2) if network_io else 0,
                'network_recv_mb': round(network_io.bytes_recv / (1024**2), 2) if network_io else 0,
            }
            
            return metrics
            
        except Exception as e:
            print(f"Error getting performance metrics: {e}")
            return {'error': str(e)}
    
    def cleanup_old_data(self, days=30):
        """Clean up data older than specified days"""
        try:
            cutoff_date = timezone.now() - timedelta(days=days)
            
            # Clean up old network usage records
            deleted_usage, _ = NetworkUsage.objects.filter(
                timestamp__lt=cutoff_date
            ).delete()
            
            # Clean up old payment records (keep for accounting)
            # deleted_payments, _ = Payment.objects.filter(
            #     payment_date__lt=cutoff_date
            # ).delete()
            
            return {
                'deleted_usage_records': deleted_usage,
                'cutoff_date': cutoff_date
            }
            
        except Exception as e:
            print(f"Error during data cleanup: {e}")
            return {'error': str(e)}

# Global instance
system_manager = SystemManager()
