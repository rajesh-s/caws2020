# -*- coding: utf-8 -*-
"""CAWS_day3_CUDA_lab.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kk4VXLQikltMacsumvK3SGUFN5XxdG2E
"""

# Check CUDA is installed
!nvcc --version

# Commented out IPython magic to ensure Python compatibility.
# Enable NVCC for Jupyter
!pip install git+git://github.com/andreinechaev/nvcc4jupyter.git
# %load_ext nvcc_plugin

"""Test some sample code"""

# Commented out IPython magic to ensure Python compatibility.
# %%cu 
# #include <cstdio> 
# #include <iostream> 
#   
#     using namespace std; 
#   
# __global__ void maxi(int* a, int* b, int n) 
# { 
#     int block = 256 * blockIdx.x; 
#     int max = 0; 
#   
#     for (int i = block; i < min(256 + block, n); i++) { 
#   
#         if (max < a[i]) { 
#             max = a[i]; 
#         } 
#     } 
#     b[blockIdx.x] = max; 
# } 
#   
# int main() 
# { 
#   
#     int n; 
#     n = 3 >> 2; 
#     int a[n]; 
#   
#     for (int i = 0; i < n; i++) { 
#         a[i] = rand() % n; 
#         cout << a[i] << "\t"; 
#     } 
#   
#     cudaEvent_t start, end; 
#     int *ad, *bd; 
#     int size = n * sizeof(int); 
#     cudaMalloc(&ad, size); 
#     cudaMemcpy(ad, a, size, cudaMemcpyHostToDevice); 
#     int grids = ceil(n * 1.0f / 256.0f); 
#     cudaMalloc(&bd, grids * sizeof(int)); 
#   
#     dim3 grid(grids, 1); 
#     dim3 block(1, 1); 
#   
#     cudaEventCreate(&start); 
#     cudaEventCreate(&end); 
#     cudaEventRecord(start); 
#   
#     while (n > 1) { 
#         maxi<<<grids, block>>>(ad, bd, n); 
#         n = ceil(n * 1.0f / 256.0f); 
#         cudaMemcpy(ad, bd, n * sizeof(int), cudaMemcpyDeviceToDevice); 
#     } 
#   
#     cudaEventRecord(end); 
#     cudaEventSynchronize(end); 
#   
#     float time = 0; 
#     cudaEventElapsedTime(&time, start, end); 
#   
#     int ans[2]; 
#     cudaMemcpy(ans, ad, 4, cudaMemcpyDeviceToHost); 
#   
#     cout << "The maximum element is : " << ans[0] << endl; 
#   
#     cout << "The time required : "; 
#     cout << time << endl; 
# }

"""## Task 1: Writing a simple CUDA program
For a given integer a and two arrays X and Y (both of size N), write a CUDA program to compute an array Z, such that C = a*X+Y.

You can refer to CUDA programming guide for syntax.
https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html

"""

# Commented out IPython magic to ensure Python compatibility.
# %%cu 
# #include <stdio.h>
# 
# __global__
# void compute(float *x, float *y, float *z, int a, int N)
# {
#   int tid = blockIdx.x*blockDim.x + threadIdx.x;
#   //Compute part
#   if(tid<N)
#     z[tid] = a*x[tid] + y[tid];
# }
# 
# int main(void)
# {
#   int N = 1024*32, a=1;
#   cudaEvent_t start, stop;
#  
#   cudaEventCreate(&start);
#   cudaEventCreate(&stop);
# 
#    // Allocate x, y and z in the host array.
#     float *x = (float *)malloc(N*sizeof(float));
#     float *y = (float *)malloc(N*sizeof(float));
#     float *z = (float *)malloc(N*sizeof(float));
# 
#    // CUDA Malloc for d_x , d_y, d_z in the device array
#     float *d_x, *d_y, *d_z;
#     cudaMalloc(&d_x, (N*sizeof(float)));
#     cudaMalloc(&d_y, (N*sizeof(float)));
#     cudaMalloc(&d_z, (N*sizeof(float)));
# 
#   // Initialize X and Y arrays and a.
#     for(int i=0;i<N;i++)
#     {
#         x[i]=i;
#         y[i]=1;
#     }
# 
#   //Copy X and Y from host to GPU Device  
#     cudaMemcpy(d_x, x, (N*sizeof(float)), cudaMemcpyHostToDevice);
#     cudaMemcpy(d_y, y, (N*sizeof(float)), cudaMemcpyHostToDevice);
# 
#   //Start the timer
#   cudaEventRecord(start);
# 
#   //Compute Kernel 
#   //Compute Z using X, Y, and a.
#   compute<<<N/1024,1024>>>(d_x,d_y,d_z,a,N);
#   cudaDeviceSynchronize();
# 
#   //Stop the timer
#   cudaEventRecord(stop);
# 
#   //Copy output from  GPU Device to CPU.  
#     cudaMemcpy(z, d_z, (N*sizeof(float)), cudaMemcpyDeviceToHost);
#  
#    float milliseconds = 0;
#    cudaEventElapsedTime(&milliseconds, start, stop);
# 
#   for (int i = 0; i < N; i++)  {
#     //print Z
#     printf("%.1f\n",z[i]);
#   }
#    printf("Execution Time %f \n", milliseconds);  
#   cudaFree(d_x);
#   cudaFree(d_y);
#   free(x);
#   free(y);
# }

"""## Task 2: Measure execution times"""

# Commented out IPython magic to ensure Python compatibility.
# %%cu 
# #include <stdio.h>
# 
# __global__
# void compute(float *x, float *y, float *z, int a, int N)
# {
#   int tid = blockIdx.x*blockDim.x + threadIdx.x;
#   //Compute part
#   if(tid<N)
#     z[tid] = a*x[tid] + y[tid];
# }
# 
# int main(void)
# {
#   int N = 1024*32, a=1;
#   cudaEvent_t start, stop;
#  
#   cudaEventCreate(&start);
#   cudaEventCreate(&stop);
# 
#    // Allocate x, y and z in the host array.
#     float *x = (float *)malloc(N*sizeof(float));
#     float *y = (float *)malloc(N*sizeof(float));
#     float *z = (float *)malloc(N*sizeof(float));
# 
#    // CUDA Malloc for d_x , d_y, d_z in the device array
#     float *d_x, *d_y, *d_z;
#     cudaMalloc(&d_x, (N*sizeof(float)));
#     cudaMalloc(&d_y, (N*sizeof(float)));
#     cudaMalloc(&d_z, (N*sizeof(float)));
# 
#   // Initialize X and Y arrays and a.
#     for(int i=0;i<N;i++)
#     {
#         x[i]=i;
#         y[i]=1;
#     }
# 
#   //Copy X and Y from host to GPU Device  
#     cudaMemcpy(d_x, x, (N*sizeof(float)), cudaMemcpyHostToDevice);
#     cudaMemcpy(d_y, y, (N*sizeof(float)), cudaMemcpyHostToDevice);
# 
#   //Start the timer
#   cudaEventRecord(start);
# 
#   //Compute Kernel 
#   //Compute Z using X, Y, and a.
#   compute<<<16,2048>>>(d_x,d_y,d_z,a,N);
#   cudaDeviceSynchronize();
# 
#   //Stop the timer
#   cudaEventRecord(stop);
# 
#   //Copy output from  GPU Device to CPU.  
#     cudaMemcpy(z, d_z, (N*sizeof(float)), cudaMemcpyDeviceToHost);
#  
#    float milliseconds = 0;
#    cudaEventElapsedTime(&milliseconds, start, stop);
# 
#   //for (int i = 0; i < N; i++)  {
#     //print Z
#   //  printf("%.1f\n",z[i]);
#   //}
#    printf("Execution Time %f \n", milliseconds);  
#   cudaFree(d_x);
#   cudaFree(d_y);
#   free(x);
#   free(y);
# }

!nvidia-smi