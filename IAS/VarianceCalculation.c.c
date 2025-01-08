#include <stdio.h>

int calculate_variance (int n){
    int i=1;
    int mean = 0;
    while (i<n+1){
        mean+=i;
        i++;
    }
    mean = mean / n; //We have calculated mean first
    int variance = 0;
    for (i=1; i<n+1;i++){
        variance += (i - mean)*(i - mean);
    }
    return variance/n;
}

int main(){
    int n;
    printf("Enter the odd number till which you wish want to take your data:");
    scanf("%d",&n);
    printf("The variance for numbers till %d is %d.",n,calculate_variance(n));
    return 0;
}