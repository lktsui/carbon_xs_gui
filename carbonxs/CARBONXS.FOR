       PROGRAM CARBON
C       
C  Least squares fitting of graphitic and disordered carbons
C
C  By:   J. N. Reimers june/93
C        Modificatied version of the LiMnO2 fitting program
C
C        Extensively modified for thick samples, 1 layer model and
C        many other assorted features in Oct/93
C  
C  All refined parameters are stored in array A(I)
C
C    A(1)   - Overall scale factor
C    A(2)   - Background constant
C    A(3)   - Background slope
C    A(4)   - Background 2TH**2 Coefficient
C    A(5)   - Background 2TH**3 Coefficient
C    A(6)   - Background 2TH**4 Coefficient
C    A(7)   - 1/S Background term
C    A(8)   - A        Cell constant
C    A(9)   - D002        Layer spacing
C    A(10)  - La        partical size in AB plane
C    A(11)  - M        # of layers along C
C    A(12)  - SM        Width of M distribution (Gets rid of ripples)
C    A(13)  - Dab        In plane strain
C    A(14)  - Del        C axis strain
C    A(15)  - Pr        Probability of a random shift
C    A(16)  - 1 layer :g        Fraction of unstrained materialn
C             2 layer :Pt        Probablilty of 3R (ABC) stacking
C    A(17)  - B        Temperature factor
C    A(18)  - PO        Preferred orientation parameter
C
        IMPLICIT NONE

        INCLUDE 'carbon.cmn'

        REAL*8  A(NPARX),COVAR(NPARX,NPARX),ALPHA(NPARX,NPARX)
        REAL*8  SIGA(NPARX),AOLD(NPARX),DYDA(NPARX,NDATX)
        REAL*8  X(NDATX),Y(NDATX),SIGY(NDATX),S(NDATX),YFIT(NDATX)
        REAL*8  TH,TH1,TH2,THR1,THR2,LC,SLC
        REAL*8  TINT,DY,DY1,DY2,DA
        REAL*8  ALAMBDA,CHISQ,OCH,OAL,EPS
        INTEGER I,J,NDAT,NPAR,RA(NPARX),MFIT,LISTA(NPARX),ITMAX,ITEST
        INTEGER NSKIP,NRAW
        CHARACTER*40 DATFILE,TITLE
        CHARACTER*50 ANAME(NPARX)

        EXTERNAL ALLINTEN

        PI=ACOS(-1.0D0)
C
C  Read control file
C
        OPEN(UNIT=1,FILE='carbon.inp',STATUS='OLD')
        READ(1,'(A40)') DATFILE
        READ(1,*) TH1,TH2,LAM,NSKIP
        READ(1,*) NPAR,NPHI,NSG,NLAYER
        READ(1,*) RDENS,L0,WD,WW,BW
        READ(1,*) ITMAX,EPS
        READ(1,*) ITEST,DA
        READ(1,10) A(1),RA(1),ANAME(1)
        AOLD(1)=A(1)
        DO I=2,NPAR
          READ(1,10) A(I),RA(I),ANAME(I)
          AOLD(I)=A(I)
        ENDDO
10      FORMAT(E12.6,T15,I1,T20,A50)
11      FORMAT(E12.3,T15,I1,T20,A50)
        CLOSE(1)
C
C  Check for errors
C
        IF (NLAYER .NE. 1 .AND. NLAYER .NE. 2) THEN
          PRINT *,'Error : Nlayer =',NLAYER,' is invalid'
          STOP
        ENDIF
        IF (RDENS .GT. 1.0D0 .OR. RDENS .LT. 0.0D0) THEN
          PRINT *,'Error : Rdens =',SNGL(RDENS),' is invalid'
          STOP
        ENDIF
        IF (A(15) .GT. 1.0D0 .OR. A(15) .LT. 0.0D0) THEN
          PRINT *,'Error : Pr =',SNGL(A(15)),' is invalid'
          STOP
        ENDIF
        IF (A(16) .GT. 1.0D0 .OR. A(16) .LT. 0.0D0) THEN
          PRINT *,'Error : Pt =',SNGL(A(16)),' is invalid'
          STOP
        ENDIF
        IF (A(13) .LT. 0.0D0) THEN
          PRINT *,'Error : Dab =',SNGL(A(13)),' < 0 is invalid'
          A(13)=0.0D0
          RA(13)=0
          PRINT *,'Dab has been reset to :',A(13)
          PRINT *,'And will NOT be refined'
        ENDIF
        IF (A(14) .LT. 0.0D0) THEN
          PRINT *,'Error : Del =',SNGL(A(14)),' < 0 is invalid'
          A(14)=0.0D0
          PRINT *,'Del has been reset to :',A(14)
        ENDIF
C
C  Rescale Pr, del and M for the 2 layer model
C
        IF (NLAYER .EQ. 2) THEN
          A(11)=A(11)/2.0D0        !M
          A(12)=A(12)/2.0D0        !SM
          A(14)=A(14)*2.0D0        !del
          A(15)=A(15)*2.0D0        !Pr
          A(16)=A(16)*2.0D0        !Pt
        ENDIF
C
C  Read the raw data
C
        
        IF (ITMAX .GT. 0) THEN
          CALL READDAT(2,DATFILE,X,S,Y,SIGY,NRAW,NDATX,THR1,THR2,TITLE)
         ELSE
          NRAW=0
          DO TH=TH1,TH2+0.01,0.05
            NRAW=NRAW+1
            IF (NRAW .GT. NDATX) STOP 'Error: Too many data points'
            X(NRAW)=TH
            S(NRAW)=2*SIN(TH*PI/180.0/2.0)/LAM
          ENDDO
        ENDIF
C
C  Cull data set to speed things up
C
        NDAT=0
        DO I=1,NRAW,NSKIP
          IF (X(I) .GE. TH1 .AND. X(I) .LE. TH2) THEN
            NDAT=NDAT+1
            X(NDAT)    = X(I)
            S(NDAT)    = S(I)
            Y(NDAT)    = Y(I)
            SIGY(NDAT) = SIGY(I)
          ENDIF
        ENDDO
C
C  Initiate the output file and write header
C
        OPEN(UNIT=3,FILE='carbon.out')

	WRITE(3,'(" Title in data file :",A40)') TITLE
        WRITE(3,20) DATFILE,LAM,NRAW,THR1,THR2,NDAT,TH1,TH2,ITMAX,
     *                    EPS,NPHI,NSG,RDENS,NLAYER,L0,BW,WD,WW
	WRITE(6,'(" Title in data file :",A40)') TITLE
        WRITE(6,20) DATFILE,LAM,NRAW,THR1,THR2,NDAT,TH1,TH2,ITMAX,
     *                    EPS,NPHI,NSG,RDENS,NLAYER,L0,BW,WD,WW
20        FORMAT (1X,"    Data file name :",A20,
     *           T45,     "       Lambda :",F8.5,
     *          /,1X," # of raw data pts :",I6 ,
     *           T40,"  Raw theta limits :",F6.2," to ",F6.2,
     *          /,1X,"# of data pts used :",I6 ,
     *           T40," Theta limits used :",F6.2," to ",F6.2,
     *          /,1X,"     Max # of it's :",I6 ,
     *           T40,"   Min delta Chi^2 :",F8.5,
     *          /,1X,"   # of pts in TCI :",I6 ,
     *           T40,"         TCI range : +/-",I4," Sigma",
     *          /,1X,"  Relative Density :",F7.3,
     *           T40,"    Stacking Model :",I2," layer",
     *          /,1X," Goniometer Radius :",F7.3,"(mm)",
     *           T40,"  X-ray Beam Width :",F7.3,"(mm)",
     *          /,1X," Sample Well Depth :",F7.3,"(mm)",
     *           T40," Sample Well Width :",F7.3,"(mm)",
     *          /)
C
C  Make a list of refined paramters
C
        MFIT=0
        DO I=1,NPAR
          IF (RA(I) .NE. 0) THEN
            MFIT=MFIT+1
            LISTA(MFIT)=I
          ENDIF
        ENDDO
C
C  Set the derivative flag,  pattern calculations are much quicker when
C  no derivatives need to be calculated.
C
        DERIV=.TRUE.
        IF (MFIT .EQ. 0 .AND. ITEST .EQ. 0) DERIV=.FALSE.
C
C  Console message
C
        IF (ITMAX .GT. 0) THEN
          WRITE (*,*) 'Iter #    Chi^2     Alambda'
          WRITE (3,*) 'Iter #    Chi^2     Alambda'
         ELSE
          WRITE (*,*) 'Beginning pattern calculation'
        ENDIF 
C
C  Do the refinement
C
        ALAMBDA=-1.0D0
        CHISQ=10000000.0
        DO I=1,ITMAX
        
        
          OCH=CHISQ
          OAL=ALAMBDA
          
          
          CALL MRQMIN(S,Y,SIGY,YFIT,NDAT,A,NPAR,LISTA,MFIT,COVAR,ALPHA,
     +                NPARX,CHISQ,ALLINTEN,ALAMBDA,DYDA)
          WRITE(*,30) I,CHISQ,ALAMBDA
          WRITE(3,30) I,CHISQ,ALAMBDA
30        FORMAT(I4,5X,F10.5,1X,E8.2)
          IF ((OCH-CHISQ)/CHISQ .LT. EPS .AND. 
     +                        ALAMBDA .LE. OAL) GOTO 40


        ENDDO

40      CONTINUE
C
C  Final call to MRQMIN to get esd's and correlation matrix
C
        IF (ITMAX .GT. 0) THEN
          ALAMBDA=0.0
          CALL MRQMIN(S,Y,SIGY,YFIT,NDAT,A,NPAR,LISTA,MFIT,COVAR,ALPHA,
     +                NPARX,CHISQ,ALLINTEN,ALAMBDA,DYDA)
C
C  Calculate sigmas for all parameters
C
          DO I=1,NPAR
            SIGA(I)=SQRT(ABS(COVAR(I,I)))
          ENDDO
C
C  Calculate the correlation matrix
C
          DO I=1,NPAR
            DO J=1,NPAR
              IF (SIGA(I)*SIGA(J) .NE. 0.0) THEN
                COVAR(I,J)=COVAR(I,J)/SIGA(I)/SIGA(J)*100.0
              ENDIF
            ENDDO
          ENDDO
C
C  Print correlation matrix
C
          WRITE(3,*)
          WRITE(3,*)'Correlation Matrix'
          WRITE(3,50) 0,(I,I=1,NPAR)
          DO I=1,NPAR
            WRITE(3,50) I,(INT(COVAR(I,J)+0.5),J=1,NPAR)
          ENDDO
50        FORMAT (1X,I2,2x,25(I4),/)
        ENDIF
C
C  Rescale Pr, del and M for the 2 layer model
C
        IF (NLAYER .EQ. 2) THEN
          A(11)=A(11)*2.0D0                !M
          A(12)=A(12)*2.0D0                !SM
          A(14)=A(14)/2.0D0                !del
          A(15)=A(15)/2.0D0                !Pr
          A(16)=A(16)/2.0D0                !pt
          SIGA(11)=SIGA(11)*2.0D0        !M
          SIGA(12)=SIGA(12)*2.0D0        !SM
          SIGA(14)=SIGA(14)/2.0D0        !del
          SIGA(15)=SIGA(15)/2.0D0        !Pr
          SIGA(16)=SIGA(16)/2.0D0        !Pt
        ENDIF
C
C  List parameters
C
        IF (ITMAX .GT. 0) THEN
          CALL LISTPAR(3,A,SIGA,AOLD,ANAME,NPAR)
          CALL LISTPAR(6,A,SIGA,AOLD,ANAME,NPAR)
          LC=A(9)*A(11)
          SLC=LC*SQRT((SIGA(9)/A(9))**2+(SIGA(11)/A(11))**2)
          WRITE(3,150) LC,SLC
          WRITE(6,150) LC,SLC
        ENDIF
150     FORMAT (//,' Lc = ',F7.1,'(',F5.1,')')
        CLOSE(3)
C
C  Write analytic and numerical derivatives,  a development tool only
C
        IF (ITEST .GT. 0) THEN
          DO I=1,NDAT
            A(ITEST)=A(ITEST)+DA
            CALL INTEN(S(I),A,DY1,SIGA,NPAR)
            A(ITEST)=A(ITEST)-2*DA
            CALL INTEN(S(I),A,DY2,SIGA,NPAR)
            A(ITEST)=A(ITEST)+DA
            DY=(DY1-DY2)/(2*DA)
            CALL INTEN(S(I),A,TINT,SIGA,NPAR)
            WRITE(*,95) X(I),DY,SIGA(ITEST),TINT
          ENDDO
        ENDIF
95      FORMAT(F6.2,3(1X,F12.5))
C
C  Write a data file

C  Rescales Parameters M, SM, del, Pr, Pt for 2 layer model calculation mode 

        IF (NLAYER .EQ. 2 .AND. ITMAX .EQ. 0) THEN
          A(11)=A(11)/2.0D0        !M
          A(12)=A(12)/2.0D0        !SM
          A(14)=A(14)*2.0D0        !del
          A(15)=A(15)*2.0D0        !Pr
          A(16)=A(16)*2.0D0        !Pt
        ENDIF

        OPEN(UNIT=1,FILE='carbon.dat')
        IF (ITMAX .EQ. 0) CALL ALLINTEN(S,A,YFIT,DYDA,NPAR,NDAT)
C
C  Undoes Rescalling of  Parameters M, SM, del, Pr, Pt for 2 layer model calculation mode 
C


        IF (NLAYER .EQ. 2 .AND. ITMAX .EQ. 0) THEN
          A(11)=A(11)*2.0D0                !M
          A(12)=A(12)*2.0D0                !SM
          A(14)=A(14)/2.0D0                !del
          A(15)=A(15)/2.0D0                !Pr
          A(16)=A(16)/2.0D0                !pt
        ENDIF        


        DO I=1,NDAT
          WRITE(1,90) X(I),INT(Y(I)),YFIT(I)
        ENDDO
90      FORMAT(F8.3,1X,I8,1X,G10.4)
        CLOSE(1)
C
C  Write new input file
C        
        OPEN(UNIT=1,FILE='carbon.inp')
        WRITE(1,'(A40)') DATFILE
        WRITE(1,100) REAL(TH1),REAL(TH2),REAL(LAM),NSKIP
        WRITE(1,110) NPAR,NPHI,NSG,NLAYER
        WRITE(1,112) RDENS,L0,WD,WW,BW
        WRITE(1,120) ITMAX,REAL(EPS)
        WRITE(1,130) ITEST,REAL(DA)
        WRITE(1,11) A(1),RA(1),ANAME(1)
        DO I=2,NPAR
          WRITE(1,10) A(I),RA(I),ANAME(I)
        ENDDO
100     FORMAT (F8.2,F8.2,F8.5,I8,8X,' Thmin   Thmax   Lambda  Nskip')
110     FORMAT (4I8,8X,' Npar    Nphi    Nsg     Nlayer')
112     FORMAT (5(1X,F7.3),' Rdens   L0      Wd      Ww      Bw')
120     FORMAT (I8,F8.5,24X,' Itmax   Eps')
130     FORMAT (I8,F8.5,24X,' Itest   Dx')
        CLOSE(1)

        STOP
        END
C***********************************************************************
C
C  Calculate scattered powder intensity and derivatives for the whole
C  pattern.
C
C    Arguments:
C      S      - Array: Magnitude of scattering vectors
C      A      - Array of parameters
C      YC     - Array: Calculated convoluted intensities
C      DYDAC  - Array: Analytic Derivatives of YFIT WRT to parameters
C      NPAR   - Number of parameters in A(I)
C      NDAT   - Number of data points in S, YC and DYDAC
C
C    From common block:
C      PI     - Just try and guess what this is
C      L0     - Goniometer radius
C      WD     - Sample well depth
C      RDENS  - Relative sample density
C
        SUBROUTINE ALLINTEN(S,A,YC,DYDAC,NPAR,NDAT)

        IMPLICIT NONE

        INCLUDE 'carbon.cmn'
        INTEGER NDAT,NPAR,I,J,JJ,JJ1,K,NJ
        REAL*8  S(NDATX),YC(NDATX),DYDAC(NPARX,NDATX),A(NPARX)
        REAL*8  Y(NDATX),DYDA(NPARX,NDATX)
        REAL*8  KERN,KK,DTH,KKMAX,FRAC,DT,THMAX,TH,KOLD,YMAX,NORM
        REAL*8  FOOT,THJ
C
C  Carbon absorbtion  **** in mm^-1 ***** NOT cm^-1
C
        MU  = 0.9D0                !Absorbtion of carbon (mm^-1)
C
C  Calculate all intensities and deriviatives
C
        DO I=1,NDAT
          CALL INTEN(S(I),A,Y(I),DYDA(1,I),NPAR)
        ENDDO
C
C  Clear arrays
C
        DO I=1,NDAT
          YC(I)=0.0D0
          IF (DERIV) THEN
            DO K=1,NPAR
              DYDAC(K,I)=0.0D0
            ENDDO
          ENDIF
        ENDDO
C
C  Figure out the theta (NOT 2theta) increment in radians NOT degrees
C
        DTH=ASIN(S(2)*LAM/2.0)-ASIN(S(1)*LAM/2.0)
C
C  Convolute
C
        DO I=1,NDAT
          TH=ASIN(S(I)*LAM/2.0D0)        !Get Theta in radians
          FOOT=1.0/SIN(TH)               !Scale factor to account for
C                                        !footprint of beam on the sample
          THMAX=WD/L0*COS(TH)            !Maximum Theta from bottom of sample
          NJ=INT(THMAX/DTH)              !# of points in convolution sum
          KOLD=1.0
          DO J=I+1,I+NJ
            THJ=TH+DTH*(J-I)
            KK=KERN(TH,THJ)
            DT=DTH*L0/COS(THJ)*(1.0+TAN(THJ)*(THJ-TH))*FOOT
            JJ=MIN(NDAT,J)
            YC(I)=YC(I) + 0.5*DT*(KK*Y(JJ)+KOLD*Y(JJ-1))
            IF (DERIV) THEN
              DO K=1,NPAR
                DYDAC(K,I)=DYDAC(K,I) + 0.5*DT*
     *                     (KK*DYDA(K,JJ)+KOLD*DYDA(K,JJ-1))
              ENDDO
            ENDIF
            KOLD=KK
          ENDDO
C
C  Pick up the tail between the last point and the end of the kernal.
C
          THJ  =TH+DTH*NJ
          DT   =(THMAX+TH-THJ)*L0/COS(THMAX)
     *         *(1.0+TAN(THMAX)*(THMAX-TH))*FOOT
          FRAC =(THMAX+TH-THJ)/DTH
          KKMAX=KERN(TH,TH+THMAX)
          JJ   =MIN(NDAT,I+NJ)
          JJ1  =MIN(NDAT,I+NJ+1)
          YMAX =FRAC*Y(JJ1) + (1-FRAC)*Y(JJ)
          YC(I)=YC(I) + 0.5*DT*(KKMAX*YMAX+KOLD*Y(JJ))
          IF (DERIV) THEN
            DO K=1,NPAR
              YMAX=FRAC*DYDA(K,JJ1) + (1-FRAC)*DYDA(K,JJ)
              DYDAC(K,I)=DYDAC(K,I) + 0.5*DT*
     *                   (KKMAX*YMAX+KOLD*DYDA(K,JJ))
            ENDDO
          ENDIF
C
C  Rescale with normalization constant
C
          NORM=2.0D0*MU*RDENS
          YC(I)=YC(I)*NORM
          DO K=1,NPAR
            DYDAC(K,I)=DYDAC(K,I)*NORM
          ENDDO
C
C  Put in fancy background function
C
        YC(I)=YC(I)+A(2)+A(3)*S(I)**1+A(4)*S(I)**2+A(5)*S(I)**3
     +                  +A(6)*S(I)**4+A(7)/S(I)
        DYDAC(2,I)=1.0
        DYDAC(3,I)=S(I)
        DYDAC(4,I)=S(I)**2
        DYDAC(5,I)=S(I)**3
        DYDAC(6,I)=S(I)**4
        DYDAC(7,I)=1.0D0/S(I)

        ENDDO

        RETURN
        END
C***********************************************************************
C
C  Kernal for the convolution routine
C
C    Arguments:
C      THI    - Measured   Theta (NOT 2theta) in radians NOT degrees.
C      THJ    - Convoluted Theta (NOT 2theta) in radians NOT degrees.
C
C    From common block:
C      PI     - Just try and guess what this is
C      RDENS  - Density of the sample relative to ideal carbon
C      L0     - Gonionmeter radius in mm
C      WD     - Sample well depth in mm
C      WW     - Sample well width in mm
C      BW     - Beam width on sample in mm
C
        FUNCTION KERN(THI,THJ)

        IMPLICIT NONE

        INCLUDE 'carbon.cmn'

        REAL*8  KERN,THI,THJ
        REAL*8  T,T1,T2,EPS
C
C  Leway for thickness cutoff
C
        EPS=1.0D-4
C
C  Theta limits
C
        IF (THI .EQ. THJ) THEN
          KERN=1.0D0
          RETURN
        ENDIF
C
C  Depth in sample
C
        T=(THJ-THI)*L0/COS(THI)
C
C  This is the default return value of the kernel if certain conditions
C  are not satisfied.
C
        KERN=0.0D0
C
C  Is T < 0, if so return KERN=0.0
C  There should be no scattering from above the sample!!!
C
        IF (T .LT. 0.0) THEN
          PRINT *,'T was < 0 !!!',T
          RETURN
        ENDIF
C
C  Is T > WD,  if so return KERN = 0.0
C
        IF (T .GT. WD + EPS) then
          PRINT *,'T was > wd',T,WD
          RETURN
        ENDIF
C
C  Is T < T1
C
        T1 = 0.5*(WW-BW/(2*SIN(THJ)))*TAN(THJ)
        IF (T .LE. T1) THEN
          KERN=EXP(-2*MU*RDENS*L0*(THJ-THI)/(SIN(THJ)*COS(THJ)))
          RETURN
        ENDIF
C
C  Is T1 < T < T2
C
        T2 = 0.5*(WW+BW/(2*SIN(THJ)))*TAN(THJ)
        IF (T .LE. T2) THEN
          KERN=EXP(-2*MU*RDENS*L0*(THJ-THI)/(SIN(THJ)*COS(THJ)))
          KERN=KERN*(T2-T)/(T2-T1)
          RETURN
        ENDIF
C
C  If we get to this point then T > T2 and there is no scattering
C  i.e. KERN = 0
C
        RETURN
        END
C***********************************************************************
C
C  Calculate scattered powder intensity at wavevector S
C
C    Arguments:
C      S     - Magnitude of scattering vector
C      A     - Array of parameters
C      YFIT  - calculated intensity
C      DYDA  - Analytic Derivatives of YFIT WRT to parameters A
C      N     - Number of parameters in A(I)
C
        SUBROUTINE INTEN(S,A,YFIT,DYDA,N)

        IMPLICIT NONE

        INTEGER NROD,N
        PARAMETER (NROD=5)

        REAL*8  YFIT,S,A(N),DYDA(N)
        REAL*8  TH,PSI,POL,DWF,ALPHA,FCARB,PHINT,PH
        REAL*8  DA,DC,DLA,DM,DSM,DDAB,DDEL,DPR,DPT,DDWF,DPO
        INTEGER H,K,HK(2,NROD),MULT(NROD),I

        INCLUDE 'carbon.cmn'
C
C  hkl's and multiplicities of the rods
C
        DATA        HK/0,0, 1,0, 1,1, 2,0, 2,1/
        DATA        MULT/1,6,6,6,12/
C
C  Polarization factor
C
        TH=ASIN(S*LAM/2.0)
        PSI=13.3*PI/180.0
        POL=0.5*(1+COS(2*TH)**2*COS(2*PSI)**2)/S
C
C  Debye Waller Factor
C
        DWF=EXP(-2.0D0*A(17)*(S/2.0D0)**2)
        DDWF=-DWF*2.0D0*(S/2.0D0)**2
C
C  Zero Yfit and derivative array
C
        YFIT=0.0
        DO I=1,N
          DYDA(I)=0
        ENDDO
C
C  Loop through all rods
C
        DO I=1,NROD
          H=HK(1,I)
          K=HK(2,I)
C
C  Calculate as much info as possible for the structure factor,  outside
C  tangent cylinder integral loop
C
          ALPHA=2*COS(2.0D0*PI/3.0D0*(H-K))*FCARB(S/2.0D0)
C
C  Do the tangent cylinder integral
C
          PH=PHINT(H,K,S,A(8),A(9),A(10),A(11),A(12),A(13),A(14),
     +       A(15),A(16),A(18),DA,DC,DLA,DM,DSM,DDAB,DDEL,DPR,DPT,DPO)
C
C  Update YFIT and all derivatives
C
          YFIT    =YFIT    +MULT(I)*POL*ALPHA**2*DWF *PH
          DYDA(8) =DYDA(8) +MULT(I)*POL*ALPHA**2*DWF *DA
          DYDA(9) =DYDA(9) +MULT(I)*POL*ALPHA**2*DWF *DC
          DYDA(10)=DYDA(10)+MULT(I)*POL*ALPHA**2*DWF *DLA
          DYDA(11)=DYDA(11)+MULT(I)*POL*ALPHA**2*DWF *DM
          DYDA(12)=DYDA(12)+MULT(I)*POL*ALPHA**2*DWF *DSM
          DYDA(13)=DYDA(13)+MULT(I)*POL*ALPHA**2*DWF *DDAB
          DYDA(14)=DYDA(14)+MULT(I)*POL*ALPHA**2*DWF *DDEL
          DYDA(15)=DYDA(15)+MULT(I)*POL*ALPHA**2*DWF *DPR
          DYDA(16)=DYDA(16)+MULT(I)*POL*ALPHA**2*DWF *DPT
          DYDA(17)=DYDA(17)+MULT(I)*POL*ALPHA**2*DDWF*PH
          DYDA(18)=DYDA(18)+MULT(I)*POL*ALPHA**2*DWF *DPO
        ENDDO
C
C  Put in scale factor
C
        DYDA(1)=YFIT
        YFIT   =A(1)*YFIT
        DO I=8,N
          DYDA(I) =A(1)*DYDA(I)
        ENDDO

        RETURN
        END
C***********************************************************************
C
C  Calculate Phi integral numerically
C
C    Arguments:
C      H,K     - Miller indicies for the rods
C      S       - Magnitude of scattering vector
C      A,D002  - Cell constants
C      LA      - Coherence length in the AB plane
C      M       - Number of layers along the C direction
C      SM      - Layer # distribution width
C      DEL     - Strain
C      PR      - Probability of random shift
C      PT      - 2layer: Probability of ABC registered stacking
C                1layer: Fraction of unstrained material
C      PO      - Preferred orientation
C      D???    - Analytic Derivatives of PHINT WRT all parameters
C
C    In common block:
C
C      NPHI    - Number of points in the numerical PHI integral
C      NSG     - Number of standard devaitions to integrate on either
C                side of a rod
C      DERIV   - Calculate derivatives flag
C      LAM     - Wavelength
C
        FUNCTION PHINT(H,K,S,A,D002,LA,M,SM,DAB,DEL,PR,PT,PO,
     +        DA,DC,DLA,DM,DSM,DDAB,DDEL,DPR,DPT,DPO)

        IMPLICIT NONE

        INCLUDE 'carbon.cmn'

        REAL*8  PHINT,S,A,D002,LA,M,SM,DAB,DEL,PR,PT,PO
        REAL*8  S0,SIG,S1,S2,PHI1,PHI2,PHI,DPHI
        REAL*8  SAFEACOS,IGRAN
        REAL*8  DA,DC,DLA,DM,DSM,DDAB,DDEL,DPR,DPT,DPO
        REAL*8  DS0DA
        INTEGER H,K,I,NPHI1
C
C  Zero everything
C
        PHINT=0.0D0
        IF (DERIV) THEN
          DA   =0.0D0
          DC   =0.0D0
          DLA  =0.0D0
          DM   =0.0D0
          DSM  =0.0D0
          DDAB =0.0D0
          DDEL =0.0D0
          DPR  =0.0D0
          DPT  =0.0D0
          DPO  =0.0D0
        ENDIF
C
C  Rod scattering vector
C
        S0=SQRT(4.0D0/3.0D0*(H**2 + K**2 + H*K))/A
        IF (DERIV) DS0DA=-S0/A
C
C  Determine integration limits in S
C
        SIG=(2.0/SQRT(3.0*PI)/LA+DAB*S0)/2.0
        S1=S0-NSG*SIG
        S2=S0+NSG*SIG
C
C  Scan through the three possible cases
C
C    No intersection
C
        IF (S .LT. S1) THEN
          RETURN
        ENDIF
C
C  Calculate Angular limits
C
        PHI1=SAFEACOS(S1/S)
        PHI2=SAFEACOS(S2/S)
        DPHI=(PHI1-PHI2)/DBLE(NPHI-1)
C
C  Full intersection
C
        IF (S .GT. S1 .AND. S .LT. S2) THEN
          PHI=-PHI1
          NPHI1=INT(2*PHI1/DPHI)+1
          DO I=1,NPHI1
            PHINT=PHINT+IGRAN(PHI,S,S0,H,K,D002,LA,M,SM,DAB,DEL,PR,PT,
     +                  PO,DA,DC,DLA,DM,DSM,DDAB,DDEL,DPR,DPT,DPO)
            PHI=PHI+DPHI
          ENDDO
        ENDIF
C
C  Two intersections
C
        IF (S .GT. S2) THEN
          PHI=PHI2
          DO I=1,NPHI
            PHINT=PHINT+IGRAN(PHI,S,S0,H,K,D002,LA,M,SM,DAB,DEL,PR,PT,
     +                  PO,DA,DC,DLA,DM,DSM,DDAB,DDEL,DPR,DPT,DPO)
            PHI=PHI+DPHI
          ENDDO
          PHI=-PHI2
          DO I=1,NPHI
            PHINT=PHINT+IGRAN(PHI,S,S0,H,K,D002,LA,M,SM,DAB,DEL,PR,PT,
     +                  PO,DA,DC,DLA,DM,DSM,DDAB,DDEL,DPR,DPT,DPO)
            PHI=PHI-DPHI
          ENDDO
        ENDIF
C
C  Scale everything by DPHI
C
        PHINT=PHINT   *DPHI
        IF (DERIV) THEN
          DA   =DA*DS0DA*DPHI
          DC   =DC      *DPHI
          DLA  =DLA     *DPHI
          DM   =DM      *DPHI
          DSM  =DSM     *DPHI
          DDAB =DDAB    *DPHI
          DDEL =DDEL    *DPHI
          DPR  =DPR     *DPHI
          DPT  =DPT     *DPHI
          DPO  =DPO     *DPHI
        ENDIF

        RETURN
        END
C***********************************************************************
C
C  Calculate integrand for PHI integral and update all derivatives
C
C    Arguments:
C      PHI    - Cylinder angle
C      S      - Magnitude of scattering vector
C      S0     - Magnitude of rod vector
C      H,K    - Miller indicies for the rod
C      D002   - Layer spacing c/2
C      LA     - Coherence length in the AB plane
C      M      - Number layers along the c direction
C      SM     - Layer # distribution width
C      DAB    - AB plane strain
C      DEL    - C axis strain
C      PT     - 2layer: Probability of ABC registered stacking
C               1layer: Fraction of unstrained material
C      PT     - Probability of ABC Stacking
C      PO     - Preferred orientation correction
C      D???   - Analytic Derivatives of IGRAN WRT all parameters
C
        FUNCTION IGRAN(PHI,S,S0,H,K,D002,LA,M,SM,DAB,DEL,PR,PT,PO,
     +        DS0,DD002,DLA,DM,DSM,DDAB,DDEL,DPR,DPT,DPO)

        IMPLICIT NONE

        REAL*8  IGRAN,PHI,S,S0,D002,LA,M,SM,DAB,DEL,PR,PT,PO
        REAL*8  L,ET,G,GMOD,ETAG,POC,CS
        REAL*8  DS0,DD002,DLA,DM,DSM,DDAB,DDEL,DPR,DPT,DPO
        REAL*8  DEDS0,DGDL,DCSDL,DLDD,DEDLA,DGDM,DGDD,DGDPR,DGDPT,DPDPO
        REAL*8  DEDAB,DGDSM
        INTEGER H,K

        INCLUDE 'carbon.cmn'

        L=S*2*D002*SIN(PHI)
        IF (DERIV) DLDD=2*S*SIN(PHI)
C
C  Calulate crystal modulation function
C
        G=GMOD(H,K,L,M,SM,DEL/(2.0D0*D002),PR,PT,DGDL,DGDM,DGDSM,
     +               DGDD,DGDPR,DGDPT)

        IF (DERIV) THEN
          IF (L .NE. 0) DGDL=DGDL-DEL*S*SIN(PHI)*DGDD/L**2
          DGDD=DGDD/(2*D002)
        ENDIF
C
C  Calculate lineshape (Gaussian)
C
        ET=ETAG(LA,S,S0,PHI,DAB,DEDS0,DEDLA,DEDAB)
C
C  Preferred Orientation Correction
C
        POC=EXP(-PO*COS(PHI)**2)
        IF (DERIV) DPDPO=-POC*COS(PHI)**2
C
C  2 Layer structure factor (I changed the factor of 4 in paper to 2,
C        it keeps the scale factors roughly the same when switching
C        between the two models)
C
        IF (NLAYER .EQ. 1) THEN
          CS=1.0D0
          IF (DERIV) DCSDL=0.0D0
         ELSE
          CS=2.0D0*COS(PI*((H-K)/3.0D0+L/2.0D0))**2
          IF (DERIV) DCSDL=-PI*SIN(2*PI*((H-K)/3.0D0+L/2.0D0))
        ENDIF
C
C  Integrand
C
        IGRAN=G*ET*POC*CS
C
C  all derivatives
C
        IF (DERIV) THEN
          DS0  =DS0  +G*DEDS0 *POC*CS
          DD002=DD002+(DGDL*CS+G*DCSDL)*ET*POC*DLDD
          DLA  =DLA  +G*DEDLA *POC*CS
          DM   =DM   +DGDM *ET*POC*CS
          DSM  =DSM  +DGDSM*ET*POC*CS
          DDAB =DDAB +G*DEDAB *POC*CS
          DDEL =DDEL +DGDD *ET*POC*CS
          DPR  =DPR  +DGDPR*ET*POC*CS
          DPT  =DPT  +DGDPT*ET*POC*CS
          DPO  =DPO  +G*ET*DPDPO*CS
        ENDIF

        RETURN
        END
C***********************************************************************
C
C  Safe Acos routine (Aviods the stupid fucking runtime DOMAIN errors)
C
        FUNCTION SAFEACOS(X)

        IMPLICIT NONE
        REAL*8  SAFEACOS,X

        IF (X .LT. -1.0) X=-1.0
        IF (X .GT.  1.0) X= 1.0
        SAFEACOS=ACOS(X)

        RETURN
        END
C***********************************************************************
C
C  Calculate Gaussian rod shape in the AB plane
C
C    Arguments:
C      L    - Coherence length in the AB plane in Angstroms
C      S    - Magnitude of scattering vector
C      S0   - Magnitude of HK rod vector
C      P    - Phi angle between scattering vector and Z axis
C      DAB  - AB plane strain
C      D??? - Analytic Derivatives
C
        FUNCTION ETAG(L,S,S0,P,DAB,DS0,DL,DDAB)

        IMPLICIT NONE
        REAL*8  ETAG,L,S,S0,P,DAB,X,W,EX
        REAL*8  DS0,DL,DDAB,DADW,DEXDW,DEXDS,A

        INCLUDE 'carbon.cmn'

        X=S*COS(P)-S0
        W=2.0/SQRT(3.0*PI)/L+DAB*S0
        EX=EXP(-2*(X/W)**2)
        A=(W-DAB*S0)/W
        ETAG=A*EX
        IF (DERIV) THEN
          DADW = DAB*S0/W**2
          DEXDW= 4*X**2/W**3*EX
          DEXDS= 4*X/W**2*EX
          DL   =-(DADW*EX+A*DEXDW)*2.0/SQRT(3.0*PI)/L**2
          DDAB = (DADW*EX+A*DEXDW)*S0 -S0 *EX/W
          DS0  = (DADW*EX+A*DEXDW)*DAB-DAB*EX/W+A*DEXDS
        ENDIF

        RETURN
        END
C***********************************************************************
C
C  Calculate Crystal Modulation Function G(s),  two layer model
C
C    Arguments:
C      H,K,L    - Miller indices for the rod
C      M        - Coherence length along c direction
C      SM       - Layer # distribution width
C      DEL      - Strain
C      PR       - Probability of a random shift
C      PT       - Probability of ABC Stacking
C      D??      - Analytic Derivatives
C
        FUNCTION GMOD(H,K,L,M,SM,DEL,PR,PT,DGDL,DGDM,DGDSM,DGDD,DGDPR
     *        ,DGDPT)

        IMPLICIT NONE
        REAL*8  GMOD,L,M,SM,DEL,PR,PT,DHK
        REAL*8  DGDL,DGDM,DGDSM,DM,DSM,DGDD,DGDPR,DGDPT
        INTEGER H,K
        COMPLEX*16 Q,GG,EHK,EL,QM,LQ,ES,E1PIL,E2PIL,EDEL
        COMPLEX*16 DQDL,DQDD,DGG,DQDPR,DQDPT

        INCLUDE 'carbon.cmn'
C
C  Kroneker delta
C
        DHK=0.0D0
        IF (H .EQ. 0 .AND. K .EQ. 0) DHK=1.0D0
C
C  Phase factors (1&2 layer model dependancy is here)
C
        E1PIL =EXP(CMPLX(0.0D0,1*PI*L))
        E2PIL=EXP(CMPLX(0.0D0,2*PI*L))
        EDEL =EXP(-2*(PI*DEL*L)**2)

        IF (NLAYER .EQ. 1) THEN
          EHK=PR*DHK + (1-PR)*COS(2.0/3.0*PI*(H-K))
          IF (PT .LT. 1.0D0) THEN
            EL =E1PIL * (  PT  +  (1-PT) * EDEL  )
           ELSE
            EL =E1PIL * EDEL
          ENDIF
         ELSE
          EHK=PR*DHK + 1-PR + PT * 
     +         (EXP(CMPLX(0,4.0D0/3.0D0*PI*(H-K)))-1.0D0)
          EL =E2PIL * EDEL
        ENDIF
C
C  Average phase factor
C        
        Q=EHK*EL
C
C  Derivatives of the phase factor
C
        IF (DERIV) THEN
          IF (NLAYER .EQ. 1) THEN
            DQDPR=(DHK-COS(2.0/3.0*PI*(H-K)))*EL
            IF (PT .LT. 1.0D0) THEN
              DQDPT= EHK * E1PIL*(1-EDEL)
              DQDD =-EHK * E1PIL*EDEL * (1-PT) * 4*(PI*L  )**2*DEL
              DQDL =Q*CMPLX(0.0D0,PI)
     +             - EHK * E1PIL*EDEL * (1-PT) * 4*(PI*DEL)**2*L
             ELSE
              DQDPT=0.0D0
              DQDD =Q*CMPLX(-4*(PI*L)**2*DEL,0.0D0)
              DQDL =Q*CMPLX(-4*(PI*DEL)**2*L,1*PI)
            ENDIF
           ELSE
            DQDPR=(DHK-1)*EL
            DQDPT=EL*(EXP(CMPLX(0,4.0D0/3.0D0*PI*(H-K)))-1.0D0)
            DQDD =Q*CMPLX(-4*(PI*L)**2*DEL,0.0D0)
            DQDL =Q*CMPLX(-4*(PI*DEL)**2*L,2*PI)
          ENDIF
        ENDIF
C
C  Modulation function (Must check for singularities)
C
        IF (REAL(Q) .EQ. 1.0D0) THEN
          GG =(M**2+SM**2)/M
          IF (DERIV) THEN
            DGG=(M**2-1)/3.0+SM**2
            DM =1-(SM/M)**2
            DSM=2*SM/M
          ENDIF
         ELSE
          LQ =LOG(Q)
          QM =EXP(M*LQ)
          ES =0.5*(SM*LQ)**2
          IF (REAL(ES) .GT. 5.0) ES=CMPLX(5.0D0,DIMAG(ES))
          ES =EXP(ES)
          GG =(1+Q)/(1-Q) + 2.0/M*Q*(QM*ES-1)/(1-Q)**2
          IF (DERIV) THEN
            DGG=2*(M*(QM*ES+1)*(Q-1)-(QM*ES-1)*(Q+1)+
     *                SM**2*QM*ES*LQ*(Q-1))/M/(Q-1)**3
            DM =DBLE(2*Q/(Q-1)**2/M**2*(QM*LQ*ES*M-QM*ES+1))
            DSM=DBLE(2.0/M*Q*QM*ES/(1-Q)**2*SM*LQ**2)
          ENDIF
        ENDIF
        GMOD =DBLE(GG/M)
        IF (DERIV) THEN
          DGDM =DM/M-DBLE(GG)/M**2
          DGDSM=DSM/M
          DGDL =DBLE(DQDL *DGG/M)
          DGDD =DBLE(DQDD *DGG/M)
          DGDPR=DBLE(DQDPR*DGG/M)
          DGDPT=DBLE(DQDPT*DGG/M)
        ENDIF

        RETURN
        END
C***********************************************************************
C
C  Read in X-ray data,  philips .UDF format
C
C  Arguments:
C    IU      - FORTRAN unit to open and read through
C    FN      - File name
C    X       - Array of 2theta values
C    S       - Array of scattering vectors
C    Y       - Array of intensities
C    SY      - Array of esd's in the intensities
C    N       - Number of data points read in
C    NX      - Maximum number of data points
C    TH1,TH2 - 2 Theta limits in the raw data file
C    TITLE   - Title line stored in data file (if data file has
C              no title line you are crazy!)
C
	SUBROUTINE READDAT(IU,FN,X,S,Y,SY,N,NX,TH1,TH2,TITLE)
	IMPLICIT NONE

	INTEGER IU,N,NX
	REAL*8	X(NX),S(NX),Y(NX),SY(NX),TH1,TH2
	INTEGER I
	CHARACTER*40 FN,TITLE

	INCLUDE 'carbon.cmn'

	PI=ACOS(-1.0D0)

	TITLE='No title in your data file!!!'

	OPEN(UNIT=2,FILE=FN,STATUS='OLD')
C
C  Now read columnar data
C
	TH1=100000
	TH2=-100000
	DO I=1,NX
	  READ(2,*,END=10) X(I),Y(I)
	  S(I) =2*SIN(X(I)*PI/180.0/2.0)/LAM
	  SY(I)=SQRT(Y(I))
	  TH1=MIN(X(I),TH1)
	  TH2=MAX(X(I),TH2) 
	ENDDO
10	N=I-1

	CLOSE(IU)

	RETURN
	END
C***********************************************************************
C
C  Write a list of refined parameters with esd's and old values
C
C  Arguments:
C    IU    - FORTRAN unit to write to
C    A     - Array of paramters
C    SA    - Array of parameter esd's
C    AO    - Array of old parameters (unrefined)
C    AN    - Array of parameter descriptions
C    N     - Number of parameters
C
        SUBROUTINE LISTPAR(IU,A,SA,AO,AN,N)

        IMPLICIT NONE

        INTEGER N,ILS,IS,I,IU
        REAL*8  A(N),SA(N),AO(N)
        REAL*8  LS,TA,SARND
        CHARACTER*50 AN(N),FMT


        WRITE(IU,*)
        WRITE(IU,*)'Final Parameters'
        WRITE(IU,*)'Old Value      New Value        (esd)',
     *                  '          Description'
        DO I=1,N
          IF (SA(I) .NE. 0) THEN
            FMT = "(E12.6,'    ',E12.6,'   ','(',E12.6,')',' ',A50)"
            WRITE(IU,FMT) AO(I),A(I),SA(I),AN(I)
          ELSE
            FMT = "(E12.6,'    ',E12.6,'                  ',A50)"
            WRITE(IU,FMT) AO(I),A(I),AN(I)
          ENDIF
        ENDDO

        RETURN
        END
C**********************************************************************
C
C  Carbon form factor
C
        FUNCTION FCARB(STL)

        REAL*8 STL,FCARB
        REAL*8 DFP,A(10)
        INTEGER I

        DATA A   /2.310000, 1.020000, 1.588600, 0.865000,0.215600,
     +                  20.843900,10.207500,0.568700,51.651200,0.000000/

        DATA DFP /-0.017/

        FCARB=DFP
        DO I=1,5
          FCARB=FCARB+A(I)*EXP(-A(I+5)*STL**2)
        ENDDO

        RETURN
        END
C******************************************************************************
C
C  Levnberg Marquite non-linear least squares fitting routine
C
      SUBROUTINE MRQMIN(X,Y,SIG,YFIT,NDATA,A,MA,LISTA,MFIT,
     *    COVAR,ALPHA,NCA,CHISQ,FUNCS,ALAMBDA,DYDA)

      IMPLICIT None
      
      INTEGER MMAX
      PARAMETER (MMAX=18)

      EXTERNAL FUNCS

      INTEGER NDATA
      INTEGER MA
      INTEGER MFIT
      INTEGER NCA
      INTEGER IHIT
      INTEGER J, K, KK
      REAL*8 CHISQ, OCHISQ, ALAMBDA
      
      
      
      REAL*8        X(NDATA),Y(NDATA),SIG(NDATA),YFIT(NDATA)
      REAL*8        A(MA),COVAR(NCA,NCA),ALPHA(NCA,NCA)
      REAL*8        ATRY(MMAX),BETA(MMAX),DA(MMAX),DYDA(MA,NDATA)
      INTEGER        LISTA(MA)
      
      

      IF(ALAMBDA.LT.0.)THEN
        KK=MFIT+1
        DO 12 J=1,MA
          IHIT=0
          DO 11 K=1,MFIT
            IF(LISTA(K).EQ.J)IHIT=IHIT+1
11        CONTINUE
          IF (IHIT.EQ.0) THEN
            LISTA(KK)=J
            KK=KK+1
          ELSE IF (IHIT.GT.1) THEN
            PAUSE 'Improper permutation in LISTA'
          ENDIF
12      CONTINUE
        IF (KK.NE.(MA+1)) PAUSE 'Improper permutation in LISTA'
        ALAMBDA=0.1
        CALL MRQCOF(X,Y,SIG,YFIT,NDATA,A,MA,LISTA,MFIT,ALPHA,BETA,NCA,
     *        CHISQ,FUNCS,DYDA)
        OCHISQ=CHISQ
        DO 13 J=1,MA
          ATRY(J)=A(J)
13      CONTINUE
      ENDIF
      
      
      DO 15 J=1,MFIT
        DO 14 K=1,MFIT
          COVAR(J,K)=ALPHA(J,K)
14      CONTINUE
        COVAR(J,J)=ALPHA(J,J)*(1.+ALAMBDA)
        DA(J)=BETA(J)
15    CONTINUE
      CALL GAUSSJ(COVAR,MFIT,NCA,DA,1,1)
      IF(ALAMBDA.EQ.0.)THEN
        CALL COVSRT(COVAR,NCA,MA,LISTA,MFIT)
        RETURN
      ENDIF
      DO 16 J=1,MFIT
        ATRY(LISTA(J))=A(LISTA(J))+DA(J)
16    CONTINUE
      CALL MRQCOF(X,Y,SIG,YFIT,NDATA,ATRY,MA,LISTA,MFIT,COVAR,DA,NCA,
     *CHISQ,FUNCS,DYDA)
      IF(CHISQ.LT.OCHISQ)THEN
        ALAMBDA=0.1*ALAMBDA
        OCHISQ=CHISQ
        DO 18 J=1,MFIT
          DO 17 K=1,MFIT
            ALPHA(J,K)=COVAR(J,K)
17        CONTINUE
          BETA(J)=DA(J)
          A(LISTA(J))=ATRY(LISTA(J))
18      CONTINUE
      ELSE
        ALAMBDA=10.*ALAMBDA
        CHISQ=OCHISQ
      ENDIF
      
      CHISQ = CHISQ
      OCHISQ = OCHISQ
C     WRITE(*,*) "3 C: ", CHISQ, "O: ", OCHISQ
      
      RETURN
      END
C******************************************************************************
C
C  Evalute ALPHA and BETA matrices
C
      SUBROUTINE MRQCOF(X,Y,SIG,YFIT,NDATA,A,MA,LISTA,MFIT,ALPHA,BETA,
     *NALP,CHISQ,FUNCS,DYDA)


      IMPLICIT None
      INTEGER MMAX
      
      INTEGER NDATA
      INTEGER MA
      INTEGER MFIT
      INTEGER NCA
      INTEGER IHIT
      INTEGER NALP
      INTEGER J, K, KK, I
      REAL*8 CHISQ, OCHISQ, ALAMBDA, D, DY, SIG2I, WT
      
      PARAMETER (MMAX=18)
      EXTERNAL FUNCS

      REAL*8        X(NDATA),Y(NDATA),SIG(NDATA),YFIT(NDATA)
      REAL*8        ALPHA(NALP,NALP),BETA(MA),DYDA(MA,NDATA),A(MA)
      INTEGER        LISTA(MFIT)

      DO 12 J=1,MFIT
        DO 11 K=1,J
          ALPHA(J,K)=0.
11      CONTINUE
        BETA(J)=0.
12    CONTINUE
      CHISQ=0.
      D=0.
      CALL FUNCS(X,A,YFIT,DYDA,MA,NDATA)
      DO 15 I=1,NDATA
        SIG2I=1./(SIG(I)*SIG(I))
        DY=Y(I)-YFIT(I)
        DO 14 J=1,MFIT
          WT=DYDA(LISTA(J),I)*SIG2I
          DO 13 K=1,J
            ALPHA(J,K)=ALPHA(J,K)+WT*DYDA(LISTA(K),I)
13        CONTINUE
          BETA(J)=BETA(J)+DY*WT
14      CONTINUE
        CHISQ=CHISQ+DY*DY*SIG2I
        D=D+SIG2I
15    CONTINUE
      CHISQ=CHISQ/DBLE(NDATA-MA)
      DO 17 J=2,MFIT
        DO 16 K=1,J-1
          ALPHA(K,J)=ALPHA(J,K)
16      CONTINUE
17    CONTINUE
      RETURN
      END
C******************************************************************************
C
C  Sort out covarience matrix
C
      SUBROUTINE COVSRT(COVAR,NCVM,MA,LISTA,MFIT)

      IMPLICIT REAL*8(A-H,O-Z)

      DIMENSION COVAR(NCVM,NCVM),LISTA(MFIT)

      DO 12 J=1,MA-1
        DO 11 I=J+1,MA
          COVAR(I,J)=0.
11      CONTINUE
12    CONTINUE
      DO 14 I=1,MFIT-1
        DO 13 J=I+1,MFIT
          IF(LISTA(J).GT.LISTA(I)) THEN
            COVAR(LISTA(J),LISTA(I))=COVAR(I,J)
          ELSE
            COVAR(LISTA(I),LISTA(J))=COVAR(I,J)
          ENDIF
13      CONTINUE
14    CONTINUE
      SWAP=COVAR(1,1)
      DO 15 J=1,MA
        COVAR(1,J)=COVAR(J,J)
        COVAR(J,J)=0.
15    CONTINUE
      COVAR(LISTA(1),LISTA(1))=SWAP
      DO 16 J=2,MFIT
        COVAR(LISTA(J),LISTA(J))=COVAR(1,J)
16    CONTINUE
      DO 18 J=2,MA
        DO 17 I=1,J-1
          COVAR(I,J)=COVAR(J,I)
17      CONTINUE
18    CONTINUE
      RETURN
      END
C******************************************************************************
C
C  Solve linear system with Gauss-Jordan elimination
C
      SUBROUTINE GAUSSJ(A,N,NP,B,M,MP)

      PARAMETER (NMAX=18)

      IMPLICIT REAL*8(A-H,O-Z)

      DIMENSION A(NP,NP),B(NP,MP),IPIV(NMAX),INDXR(NMAX),INDXC(NMAX)

      DO 11 J=1,N
        IPIV(J)=0
11    CONTINUE
      DO 22 I=1,N
        BIG=0.
        DO 13 J=1,N
          IF(IPIV(J).NE.1)THEN
            DO 12 K=1,N
              IF (IPIV(K).EQ.0) THEN
                IF (ABS(A(J,K)).GE.BIG)THEN
                  BIG=ABS(A(J,K))
                  IROW=J
                  ICOL=K
                ENDIF
              ELSE IF (IPIV(K).GT.1) THEN
                WRITE(*,*) "Singular Matrix."
                PAUSE 'Singular matrix'
              ENDIF
12          CONTINUE
          ENDIF
13      CONTINUE
        IPIV(ICOL)=IPIV(ICOL)+1
        IF (IROW.NE.ICOL) THEN
          DO 14 L=1,N
            DUM=A(IROW,L)
            A(IROW,L)=A(ICOL,L)
            A(ICOL,L)=DUM
14        CONTINUE
          DO 15 L=1,M
            DUM=B(IROW,L)
            B(IROW,L)=B(ICOL,L)
            B(ICOL,L)=DUM
15        CONTINUE
        ENDIF
        INDXR(I)=IROW
        INDXC(I)=ICOL
        IF (A(ICOL,ICOL).EQ.0.) THEN
            WRITE(*,*) 'Singular matrix.'
            PAUSE 'Singular matrix'
        ENDIF


        PIVINV=1./A(ICOL,ICOL)
        A(ICOL,ICOL)=1.
        DO 16 L=1,N
          A(ICOL,L)=A(ICOL,L)*PIVINV
16      CONTINUE
        DO 17 L=1,M
          B(ICOL,L)=B(ICOL,L)*PIVINV
17      CONTINUE
        DO 21 LL=1,N
          IF(LL.NE.ICOL)THEN
            DUM=A(LL,ICOL)
            A(LL,ICOL)=0.
            DO 18 L=1,N
              A(LL,L)=A(LL,L)-A(ICOL,L)*DUM
18          CONTINUE
            DO 19 L=1,M
              B(LL,L)=B(LL,L)-B(ICOL,L)*DUM
19          CONTINUE
          ENDIF
21      CONTINUE
22    CONTINUE
      DO 24 L=N,1,-1
        IF(INDXR(L).NE.INDXC(L))THEN
          DO 23 K=1,N
            DUM=A(K,INDXR(L))
            A(K,INDXR(L))=A(K,INDXC(L))
            A(K,INDXC(L))=DUM
23        CONTINUE
        ENDIF
24    CONTINUE
      RETURN
      END
