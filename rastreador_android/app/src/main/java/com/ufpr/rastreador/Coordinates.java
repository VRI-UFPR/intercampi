/*
 *  Rastreador do Intercampi UFPR
 *  Copyright (C) 2025 Visao Robotica e Imagem (VRI)
 *  - Felipe Gustavo Bombardelli <felipebombardelli@gmail.com>
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 * * */

// =================================================================================================
//  Header
// =================================================================================================

package com.ufpr.rastreador;

// =================================================================================================
//  class Coordinates
// =================================================================================================

public class Coordinates {
    public String id;
    public double lat;
    public double log;

    /** Construtor
     *
     * @param id
     * @param latitude
     * @param longitude
     */
    public Coordinates(String id, double latitude, double longitude) {
        this.id = id;
        this.lat = latitude;
        this.log = longitude;
    }
}