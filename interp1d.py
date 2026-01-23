import numpy as np

def interp1d (x, y, fx) :
#------------------------
    '''
    REMARK
        extrapolates : takes last value   

    METHOD
                             o 
                             |
              o              |
              |     o     fx(2)
           fx(0)    |        |
              |  fx(1)       |                       =>
              |     |        |                                  
    ----------|-----|--------|----------------         --------|-----|-------
            x(0)  x(1)     x(2)                              y(0)  y(1)     

    MODIFICATIONS
        (2025-12-15) replaced '<' b '<=' and '>' by '>='
             if ( y[iy] <= xmin ) :   # lt
             elif ( y[iy] >= xmax ) :  # gt            
    '''

# 
#    print('+++ interp1d +++')
#    print('x  : ', x)
#    print('fx : ', fx)
#    print('y  : ', y) 

#   x-array and fx-array should have the same length    
    if ( len(x) != len(fx) ) :        
        print('x and fx have different size')
        print('x  : ',      x)
        print('fx : ',     fx)  
        print('len(x)  : ', len( x))
        print('len(fx) : ', len(fx))  
        quit()
#
# orientation 'down' if decreasing values of x
# orientation 'up'   if increasing values of x
    if ( len(x) > 1 ) : 
        if (   ( x[1] - x[0] ) > 0. ) : xorientation='up'  # gt
        elif ( ( x[0] - x[1] ) > 0. ) : xorientation='down'
    else :
        xorientation='up' # if only one point available

    if ( len(y) > 1 ) : 
        if (   ( y[1] - y[0] ) > 0. ) : yorientation='up'  # gt
        elif ( ( y[0] - y[1] ) > 0. ) : yorientation='down'
    else :
        yorientation='up' # if only one point available

    nx=len(x)
    ny=len(y)

    fy = np.zeros((ny), dtype=float)

    xmin = min(x)
    xmax = max(x)
   
    first=1

    for iy in range(0,ny) : # loop over y-values
        if ( y[iy] <= xmin ) :   # lt
            if   ( xorientation == 'up' )   : fy[iy] = fx[0]
            elif ( xorientation == 'down' ) : fy[iy] = fx[nx-1]
            else :
                print('no orientation recognized') 
                quit()                        
            first=1 
        elif ( y[iy] >= xmax ) :  # gt
            if   ( xorientation == 'up' )   : fy[iy] = fx[nx-1]
            elif ( xorientation == 'down' ) : fy[iy] = fx[0]
            else : 
                print('no orientation recognized') 
                quit()
            first=1 
        elif ( first == 1 ) : 
            for ix in range (0,nx-1) :
                if ( min([x[ix],x[ix+1]]) <= y[iy] and y[iy] <= max([x[ix],x[ix+1]]) ) :   # le , le
                     fy[iy] = fx[ix]   * ( x[ix+1] - y[iy] ) / ( x[ix+1] - x[ix] ) \
                            + fx[ix+1] * ( y[iy]   - x[ix] ) / ( x[ix+1] - x[ix] )
                     break # ix will stay on used value
            first=0  
        else : 
            found=0
            while ( found ==0 ) :              
                if ( min([x[ix],x[ix+1]]) <= y[iy] and y[iy] <= max([x[ix],x[ix+1]]) ) :   # le , le
                     fy[iy] = fx[ix]   * ( x[ix+1] - y[iy] ) / ( x[ix+1] - x[ix] ) \
                            + fx[ix+1] * ( y[iy]   - x[ix] ) / ( x[ix+1] - x[ix] )
                     found=1
                else :
                   if ( xorientation == yorientation ) : ix=ix+1
                   else                                : ix=ix-1
#
#    print('fy : ', fy)
    
#    print('--- interp1d ---')

    return fy
