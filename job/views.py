from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer

from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from django.db.models import Avg, Count, Min, Sum, Max
from .filters import JobFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


# Create your views here.


@api_view(['GET'])
def getAllJobs(request):
    # jobs = Job.objects.all()

    filters = JobFilter(request.GET, queryset=Job.objects.all().order_by('-id'))

    count = filters.qs.count()

    # pagination
    results_per_page = 10
    paginator = PageNumberPagination()
    paginator.page_size = results_per_page

    queryset = paginator.paginate_queryset(filters.qs, request)

    serializer = JobSerializer(queryset, many=True)

    # return Response(serializer.data)
    return Response({'count': count, 'resPerPage': results_per_page, 'jobs': serializer.data})


@api_view(['GET'])
def getJob(request, pk):
    # job = Job.objects.get(id=pk)
    job = get_object_or_404(Job, id=pk)

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createJob(request):
    request.data['user'] = request.user
    data = request.data

    job = Job.objects.create(**data)

    """
    job = Job.objects.create(
        title=data['title'],
        company=data['company'],
        description=data['description'],
        salary=data['salary'],
        location=data['location'],
        email=data['email'],
        phone=data['phone'],
        url=data['url'],
        date=data['date'],
    )
    """
    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateJob(request, pk):
    job = get_object_or_404(Job, id=pk)

    if job.user != request.user:
        return Response({'message': 'You are not authorized to update this job'}, status=status.HTTP_403_FORBIDDEN)

    job.title = request.data['title']
    job.description = request.data['description']
    job.email = request.data['email']
    job.address = request.data['address']
    job.job_type = request.data['job_type']
    job.education = request.data['education']
    job.experience = request.data['experience']
    job.industry = request.data['industry']
    job.salary = request.data['salary']
    job.positions = request.data['positions']
    job.company = request.data['company']
    job.city = request.data['city']
    job.state = request.data['state']
    job.country = request.data['country']
    # job.last_date = request.data['last_date']
    # job.point = request.data['point']
    # job.user = request.data['user']

    job.save()

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteJob(request, pk):
    job = get_object_or_404(Job, id=pk)
    if job.user != request.user:
        return Response({'message': 'You are not authorized to update this job'}, status=status.HTTP_403_FORBIDDEN)

    job.delete()

    return Response({'message': 'Job deleted successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getTopicStats(request, topic):
    args = {"title__icontains": topic}
    jobs = Job.objects.filter(**args)

    if len(jobs) == 0:
        return Response({'message': f'Nothing found for {topic}'.format(topic=topic)}, status=status.HTTP_200_OK)

    # Get the average salary
    stats = jobs.aggregate(
        total_jobs=Count('title'),
        avg_positions=Avg('positions'),
        min=Min('salary'),
        max=Max('salary'),
        avg_salary=Avg('avg_salary')
    )

    return Response(stats, status=status.HTTP_200_OK)
