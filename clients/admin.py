'''
# Billing System - Africa Online Networks
# Copyright (c) 2025 Martin Mutinda. All Rights Reserved.
# 
# Proprietary Software - Unauthorized copying, modification, distribution,
# or use of this software via any medium is strictly prohibited.
# 
# This software is the confidential and proprietary information of
# Martin Mutinda ("Confidential Information"). You shall not disclose
# such Confidential Information and shall use it only in accordance
# with the terms of the license agreement.
# 
# For licensing inquiries:
# 📧 Email: martinmutinda@africaonlinenetworks.co.ke
# 📞 Phone: +254 706 315 742
# 
# Developed with ❤️ by Martin Mutinda
'''

from django.contrib import admin
from .models import Client, Payment, ServicePlan

admin.site.register(Client)
admin.site.register(Payment)
admin.site.register(ServicePlan)

