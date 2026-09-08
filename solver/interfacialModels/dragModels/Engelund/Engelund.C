/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | Copyright (C) 2011 OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "Engelund.H"
#include "addToRunTimeSelectionTable.H"

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

namespace Foam
{
    defineTypeNameAndDebug(Engelund, 0);

    addToRunTimeSelectionTable
    (
        dragModel,
        Engelund,
        dictionary
    );
}


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::Engelund::Engelund
(
    const dictionary& interfaceDict,
    const phaseModel& phases,
    const volScalarField& rhof,
    const volScalarField& nuf
)
:
    dragModel(interfaceDict, phases, rhof, nuf)
{}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

Foam::Engelund::~Engelund()
{}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

Foam::tmp<Foam::volScalarField> Foam::Engelund::K
(
    const volScalarField& Ur
) const
{
    volScalarField beta(max(scalar(1) - alphas_, scalar(1.0e-6)));
    volScalarField Cds
    (
    (phases_.aE()*alphas_*max(alphas_, scalar(1.0e-6))/beta
    + max(alphas_, scalar(1.0e-6))/scalar(0.6)*phases_.bE()*Ur*phases_.d()
    /(nuf_*beta*beta))
    );

    return max(Cds, scalar(1.0e-6))*nuf_*rhof_/sqr(phases_.d());
}

// ************************************************************************* //
