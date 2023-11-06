from functools import partial
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.db import models
from apscheduler.triggers.cron import CronTrigger
from foodiehotspots.schedulers import RestaurantScheduler
import time

scheduler = None #스케줄러 전역 변수로 설정

def start():
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')  # 시간대 설정
    # DjangoJobStore : django 데이터베이스를 사용하여 스케쥴링 작업 저장 및 관리
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    # 이전 스케줄이 완료될 때까지 대기할 시간(초) 설정
    wait_time = 1000
    job1 = partial(RestaurantScheduler.restaurant_scheduler, RestaurantScheduler())
    # job2 = partial(RestaurantScheduler.save, RestaurantScheduler())
    # scheduler.add_job(job1, 'cron',hour=2,misfire_grace_time=wait_time)  # 2시 실행(default)
    scheduler.add_job(job1, 'cron', minute='*',misfire_grace_time=wait_time) #!매분 실행으로 테스트
    scheduler.start()
    
