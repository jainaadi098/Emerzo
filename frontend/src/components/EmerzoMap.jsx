import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for Marker Icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

function Recenter({ lat, lng }) {
  const map = useMap();
  useEffect(() => {
    if (lat && lng) map.flyTo([lat, lng], 14, { duration: 2 });
  }, [lat, lng, map]);
  return null;
}

export default function EmerzoMap({ lat, lng, hospitals = [] }) {
  const safeLat = lat || 20.5937;
  const safeLng = lng || 78.9629;

  return (
    <div className="h-full w-full">
      <MapContainer center={[safeLat, safeLng]} zoom={13} style={{ height: "100%", width: "100%" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution='&copy; OpenStreetMap' />
        <Recenter lat={lat} lng={lng} />
        {lat && lng && <Marker position={[lat, lng]}><Popup>📍 You are here</Popup></Marker>}
        {hospitals.map((h, index) => (
          <Marker key={index} position={[h.lat, h.lng]}><Popup>🏥 {h.name}</Popup></Marker>
        ))}
      </MapContainer>
    </div>
  );
}