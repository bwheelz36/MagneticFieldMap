//
// ********************************************************************
// *                                                                  *
// * This  code  implementation is the  intellectual property  of the *
// * TOPAS collaboration.                                             *
// * Use or redistribution of this code is not permitted without the  *
// * explicit approval of the TOPAS collaboration.                    *
// * Contact: Joseph Perl, perl@slac.stanford.edu                     *
// *                                                                  *
// ********************************************************************
//

#ifndef TsMagneticFieldMap2_hh
#define TsMagneticFieldMap2_hh

#include "TsVMagneticField.hh"

#include "G4AffineTransform.hh"

#include <vector>

class TsMagneticFieldMap2 : public TsVMagneticField
{
public:
	TsMagneticFieldMap2(TsParameterManager* pM, TsGeometryManager* gM,
					   TsVGeometryComponent* component);
	~TsMagneticFieldMap2();

	void GetFieldValue(const double p[3], double* Field) const;
	void ResolveParameters();

private:
	// Physical limits of the defined region
	G4double fMinX, fMinY, fMinZ, fMaxX, fMaxY, fMaxZ;

	// Physical extent of the defined region
	G4double fDX, fDY, fDZ;

	// Allows handling of either direction of min and max positions
	G4bool fInvertX, fInvertY, fInvertZ;

	// Dimensions of the table
	G4int fNX, fNY, fNZ;

	// Storage for the table
	std::vector< std::vector< std::vector< double > > > fFieldX;
	std::vector< std::vector< std::vector< double > > > fFieldY;
	std::vector< std::vector< std::vector< double > > > fFieldZ;

	// Affine transformation to the world to resolve the position/rotation
	// when a daughter is placed in a mother holding the field
	G4AffineTransform fAffineTransf;
};

#endif
