/*---------------------------------------------------------------------------*\
Copyright (C) 2024 Antoine Mathieu, Cyrille Bonamy, Julien Chauchat,
                   Tian-Jian Hsu and contributors

License
    This file is part of SedInterFOAM.

    SedInterFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SedFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with SedInterFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

// Cell gradient of alphaw
volVectorField gradGamma(fvc::grad(gamma));;

// Interpolated face-gradient of alphaw
surfaceVectorField gradGammaf(fvc::interpolate(gradGamma));

// Face unit interface normal
surfaceVectorField  nHatfv(gradGammaf/(mag(gradGammaf) + deltaN));

const volScalarField::Boundary& gammabound = gamma.boundaryField();
//const volScalarField::Boundary& alphasbound = alphas.boundaryField();
const volScalarField::Boundary& voidFracbound = voidFrac.boundaryField();
const volVectorField::Boundary& Ubound = U.boundaryField();

const fvBoundaryMesh& boundary = mesh.boundary();

forAll(boundary, patchi)
{
    if (isA<alphaContactAngleTwoPhaseFvPatchScalarField>(gammabound[patchi]))
    {
        const alphaContactAngleTwoPhaseFvPatchScalarField& acap =
            refCast<const alphaContactAngleTwoPhaseFvPatchScalarField>
            (voidFracbound[patchi]);

        fvsPatchVectorField& nHatp = nHatfv.boundaryFieldRef()[patchi];

        scalarField theta1
        (
            degToRad() * (180 - acap.theta(Ubound[patchi], nHatp))
        );
        
        vectorField nf
        (
            boundary[patchi].nf()
        );

        // Reset nHatPatch to correspond to the contact angle

        scalarField a12(nHatp & nf);

        scalarField b1(cos(theta1));

        scalarField b2(nHatp.size());

        forAll(b2, facei)
        {
            b2[facei] = Foam::cos(Foam::acos(a12[facei]) - theta1[facei]);
        }

        scalarField det(1.0 - a12*a12);

        scalarField a((b1 - a12*b2)/det);
        scalarField b((b2 - a12*b1)/det);

        nHatp = a*nf + b*nHatp;
        nHatp /= (mag(nHatp) + deltaN.value());
    }
}

nHatf = nHatfv & mesh.Sf();

Kg = -fvc::div(nHatf);

//volScalarField limitedAlphas(max(alphas, scalar(0)));
volScalarField limitedVoidFrac(max(voidFrac, scalar(0)));

sigma = (limitedVoidFrac*sigmagf)/(limitedVoidFrac + SMALL);
