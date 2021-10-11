
# Matrix header files
## Constructor :

*  ###  Matrix()

   Get a Matrix variable
* ### Matrix( M , N )

  initialize Matrix with M rows , N columns
* ### Matrix( N , 'I' )

  initialize into  N-order Identity Matrix
* ### Matrix( Matrix M_ )

  make a copy of Matrix "M_"
* ### Matrix( vector<vector<int > > vec_)

  initialize Matrix with 2D vector "vec_"
## Input / Output :
by overloading i/o stream operator , which is convinence to input data
* ### cin>> Matrix_Variable ;

  Output " M Rows , N Columns " at first , then input your Matrx

* ### cout<<Matrix_Variable;

  Output Matrix in the following form 

>     Eg : Matrix with 2 row , 3 columns
M(1,1) M(1,2) M(1,3)
>
M(2,1) M(2,2) M(2,3)


## Member Funciton :
M represent Matrix_Variable in the following description

## Funciton return variable

* ### M.Delta()

  return interger value of Determinant of Matrix 
* ### M.Adjugate()
  return 2D vector  of Adjugate of Matrix 
* ### M.Inverse()
  return 2D vector  of Inverse of Matrix 
## Void Funciton
* ### M.Resize( M , N)

  void function , resize Matrix into M rows , N columns
* ### M.Get_Determinant()
  void funciton , calculate Determinant of Matrix and store in Matrix object
* ### M.Get_Adjugate()
  void funciton , calculate Adjugate of Matrix and store in Matrix object
* ### M.Get_Inverse()
  void funciton , calculate Inverse of Matrix and store in Matrix object
## Calculation :
the following A,B,C,D...variable represent Matrix_Variable
* ### A=B 
assign B to A 
* ### A+=B 
addition
* ### C=A+B 
* ### A-=B 
subtraction
* ### C=A-B 
* ### A*=B 
A multiplied by B
* ### C=A*B
## For Determinant,Adjugate,Inverse of Matrix :
need to process data before output

Eg: before output Determinant of Matrix
>      A.Get_Determinant();
>      cout<<A.Delta();

Eg: before output Adjugate of Matrix
>      A.Get_Adjugate();
>      cout<<A.Adjugate();

Eg: before output Inverse of Matrix
>      A.Get_Determinant();
>      A.Get_Adjugate();
>      A.Get_Inverse();
>      cout<<A.Inverse();


