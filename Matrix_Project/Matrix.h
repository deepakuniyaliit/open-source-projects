#include<iostream>
#include<cmath>
#include<vector>
#include<utility>
using namespace std;
/*---- N-order Determinant ----*/
int Det(vector<vector<int> > vec){
  int n=vec.size();
  if(n==2){
    return vec[0][0]*vec[1][1]-vec[0][1]*vec[1][0];
  }
  int ret=0;
  vector<vector<int> > V(n-1,vector<int>(n-1));
  for(int i=0,i_=0,outer,k=1;i<n;i++,k*=-1){
    outer=vec[0][i];
    for(int r=1;r<n;r++){
      for(int c=0,c_=0;c<n;c++){
        if(i==c) continue;
        V[r-1][c_]=vec[r][c];
        c_++;
      }
    }
    ret+=k*outer*Det(V);
  }
  return ret;
}
/*---- calculating N-order Adjugate Matrix ----*/
int delta(vector<vector<int> > vec){
  int n=vec.size();
  if(n==2){
    return vec[0][0]*vec[1][1]-vec[0][1]*vec[1][0];
  }
  int ret=0;
  vector<vector<int> > V(n-1,vector<int>(n-1));
  for(int i=0,i_=0,outer,k=1;i<n;i++,k*=-1){
    outer=vec[0][i];
    for(int r=1;r<n;r++){
      for(int c=0,c_=0;c<n;c++){
        if(i==c) continue;
        V[r-1][c_]=vec[r][c];
        c_++;
      }
    }
    ret+=k*outer*delta(V);
  }
  return ret;
}
vector<vector<int> > Adj(vector<vector<int> > A){
  int n=A.size(),k=1;
  vector<vector<int> > ret(n,vector<int>(n));
  if(n==2){
    ret=A;
    swap(ret[0][0],ret[1][1]);
    ret[0][1]*=-1;
    ret[1][0]*=-1;
    return ret;
  }
  vector<vector<int> > cur(n-1,vector<int>(n-1));
  for(int i=0;i<n;i++,k*=-1){
    for(int j=0;j<n;j++,k*=-1){
      for(int r=0,r_=0;r<n;r++){
        if(r==i) continue;
        for(int c=0,c_=0;c<n;c++){
          if(c==j) continue;
          cur[r_][c_]=A[r][c];
          c_++;
        }
        r_++;
      }
      ret[i][j]+=k*delta(cur);
    }
  }
  return ret;
}
/*---- Matrix main part ----*/
inline int GCD(int a,int b){
  if(a<b) swap(a,b);
  if(b==0) return a;
  return GCD(b,a%b);
}
inline int t(int a,int b){
  return (a>0 ? (b>0 ? 1:-1):(b<0 ? 1:-1));
}
inline void Fraction(pair<int,int> &p){
  if(p.first==0||p.second==0){
    p.first=0,p.second=0;
    return;
  }
  int d=GCD(abs( p.first ),abs( p.second ) );
  p.first/=d,p.second/=d;
  p.first=t(p.first,p.second)*abs(p.first),p.second=abs(p.second);
}

class Matrix{
    private:
        int M_m,M_n,M_Delta;
	    bool Invertible;
	    vector<vector<int> > M_Data;
	    vector<vector<int> > M_Adj;
	    vector<vector<pair<int,int> > > M_Inv;

    public:
        Matrix(int m=0,int n=0);
        Matrix(const Matrix &M);
        Matrix(int n,char ch);
        Matrix(vector<vector<int> > vec);
        void Resize(int m,int n);
        void Get_Inverse();
        void Get_Adjugate();
        void Get_Determinant();
        int Delta(){return M_Delta;};
        vector<vector<int> > Adjugate(){return M_Adj;};
	    vector<vector<pair<int,int> > > Inverse(){return M_Inv;};
        Matrix &operator=(const Matrix &other);
        Matrix &operator+=(const Matrix &other);
        Matrix &operator-=(const Matrix &other);
        Matrix &operator*=(const Matrix &other);
        Matrix  &operator*=(const int &K);
        bool operator==(const Matrix &other);
        bool operator!=(const Matrix &other);
        friend istream & operator>>(istream &intput,Matrix &M);
        friend ostream & operator<<(ostream &output,const Matrix &M);
};
istream & operator >>(istream &input,Matrix &M){
    cout<<M.M_m<<" rows , "<<M.M_n<<"columns \n";
    for(int i=0;i<M.M_m;i++){
        for(int j=0;j<M.M_n;j++){
            input>>M.M_Data[i][j];
        }
    }
    return input;
}
ostream & operator <<(ostream &output,const Matrix &M){
    for(int i=0;i<M.M_m;i++){
        for(int j=0;j<M.M_n;j++){
            output<<M.M_Data[i][j]<<" ";
        }
        output<<"\n";
    }
    return output;
}
ostream & operator <<(ostream &output,vector<vector<int> > vec){
    for(auto i:vec){
        for(auto j:i){
            output<<j<<" ";
        }
        output<<"\n";
    }
    return output;
}
ostream & operator <<(ostream &out,vector<vector<pair<int,int> > > vec){
    for(auto i:vec){
    for(auto j:i){
      if(j.first==0){
        out<<0<<' ';
      }
      else if(j.second==1){
        out<<j.first<<' ';
      }
      else{
        out<<j.first<<'/'<<j.second<<' ';
      }
    }
    out<<'\n';
  }
  return out;
}
Matrix& Matrix::operator=(const Matrix &other){
    M_m=other.M_m,M_n=other.M_n,M_Delta=other.M_Delta;
    Invertible=other.Invertible;
    M_Data=other.M_Data,M_Adj=other.M_Adj;
    if(Invertible) M_Inv=other.M_Inv;
    return *this;
}
Matrix& Matrix::operator+=(const Matrix &other){
    if(M_n!=other.M_n||M_m!=other.M_m){
        cout<<"can't be added\n";
        return *this;
    }
    for(int i=0;i<M_m;i++){
        for(int j=0;j<M_n;j++){
            M_Data[i][j]+=other.M_Data[i][j];
        }
    }
    return *this;
}
Matrix operator+(const Matrix &A,const Matrix &B){
    Matrix temp(A);
    temp+=B;
    return temp;
}
Matrix& Matrix::operator-=(const Matrix &other){
    if(M_n!=other.M_n||M_m!=other.M_m){
        cout<<"can't be subtracted\n";
        return *this;
    }
    for(int i=0;i<M_m;i++){
        for(int j=0;j<M_n;j++){
            M_Data[i][j]+=other.M_Data[i][j];
        }
    }
    return *this;
}
Matrix operator-(const Matrix &A,const Matrix &B){
    Matrix temp(A);
    temp-=B;
    return temp;
}
Matrix& Matrix::operator*=(const Matrix &other){
    if(M_n!=other.M_m){
        cout<<"can't be multiplied\n";
        return *this;
    }
    int m=M_m,p=other.M_n,n=M_n;
    Matrix temp(m,p);
    for(int i=0;i<m;i++){
        for(int j=0;j<p;j++){
            for(int k=0;k<n;k++){
                temp.M_Data[i][j]+=M_Data[i][k]*other.M_Data[k][j];
            }
        }
    }
    *this=temp;
    return *this;
}
Matrix& Matrix::operator*=(const int &K){
    for(int i=0;i<M_m;i++){
        for(int j=0;j<M_n;j++){
            M_Data[i][j]*=K;
        }
    }
    return *this;
}
Matrix operator*(const Matrix &A,const Matrix &B){
    Matrix temp(A);
    temp*=B;
    return temp;
}
Matrix operator*(const Matrix &A,const int K){
    Matrix temp(A);
    temp*=K;
    return temp;
}
Matrix operator*(const int K,const Matrix &A){
    Matrix temp(A);
    temp*=K;
    return temp;
}
bool Matrix::operator==(const Matrix &other){
    if(M_n!=other.M_n || M_m!=other.M_m) return false;
    for(int i=0;i<M_m;i++){
        for(int j=0;j<M_n;j++){
            if(M_Data[i][j]!=other.M_Data[i][j]) return false;
        }
    }
    return true;
}
bool Matrix::operator!=(const Matrix &other){
    return !(*this!=other);
}
void Matrix::Get_Determinant(){
    M_Delta=Det(M_Data);
    Invertible=(M_Delta==0||M_n!=M_m ? false:true);
}
void Matrix::Get_Adjugate(){
    M_Adj=Adj(M_Data);
}
void Matrix::Get_Inverse(){
    if(Invertible){
        int n=M_n;
        vector<vector<pair<int,int> > > ret(n,vector<pair<int,int>>(n));
        for(int i=0;i<n;i++){
            for(int j=0;j<n;j++){
              ret[i][j]={M_Adj[i][j],M_Delta};
              Fraction(ret[i][j]);
            }
        }
        M_Inv=ret;
    }
}
Matrix Pow(Matrix base,int n){
    if(n==1) return base;
    else if(n%2==0){
        Matrix temp=Pow(base,n/2);
        return temp*temp;
    }
    return base*Pow(base,n-1);
}
Matrix::Matrix(int m,int n){
    M_m=m,M_n=n;
    M_Data.resize(m,vector<int>(n,0));
}
Matrix::Matrix(const Matrix &M){
    *this=M;
}
void Matrix::Resize(int m,int n){
    M_m=m,M_n=n;
    M_Data.resize(m,vector<int>(n,0));
}
Matrix::Matrix(int n,char ch){
    if(ch=='I'){
        M_n=n,M_m=n;
        M_Data.resize(n,vector<int>(n,0));
        for(int i=0;i<n;i++){
            for(int j=0;j<n;j++){
                M_Data[i][j]=(i==j ? 1:0);
            }
        }
    }
    else{
        M_n=n,M_m=n;
        M_Data.resize(n,vector<int>(n,0));
    }
}
Matrix::Matrix(vector<vector<int> > vec){
    M_m=vec.size();
    M_n=vec[0].size();
    M_Data=vec;
}