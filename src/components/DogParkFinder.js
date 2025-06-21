import React from "react";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";

const dogParks = [
  {
    name: "Tompkins Square Dog Run",
    location: "East 10th St, New York, NY 10009",
    features: [
      "Double-Gated Entry/Exit",
      "Off-Leash Area",
      "Water Stations/Fountains",
      "Waste Disposal Stations",
      "Separate Areas for Large and Small/Shy Dogs"
    ],
    image: "https://images.unsplash.com/photo-1507146426996-ef05306b995a?auto=format&fit=crop&w=900&q=60"
  },
  {
    name: "East River Park Dog Run",
    location: "FDR Dr & E 10th St, New York, NY 10009",
    features: [
      "Double-Gated Entry/Exit",
      "Off-Leash Area",
      "Water Stations/Fountains",
      "Waste Disposal Stations"
    ],
    image: "https://images.unsplash.com/photo-1560807707-8cc77767d783?auto=format&fit=crop&w=900&q=60"
  },
  {
    name: "Madison Square Park Dog Run",
    location: "Madison Ave & E 23rd St, New York, NY 10010",
    features: [
      "Double-Gated Entry/Exit",
      "Off-Leash Area",
      "Water Stations/Fountains",
      "Waste Disposal Stations",
      "Shaded Areas",
      "Benches for Owners"
    ],
    image: "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?auto=format&fit=crop&w=900&q=60"
  }
];

export default function DogParkFinder() {
  return (
    <div className="min-h-screen bg-blue-100 p-6 font-sans">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-blue-900 mb-8">
          🐶 Best Dog Parks in NYC
        </h1>
        
        <p className="text-center text-blue-700 mb-8 text-lg">
          Discover the perfect spot for your furry friend to play and socialize!
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {dogParks.map((park, index) => (
            <Card key={index} className="bg-white shadow-lg rounded-2xl overflow-hidden hover:shadow-xl transition-shadow duration-300">
              <img 
                src={park.image} 
                alt={`${park.name} - Dog Park`} 
                className="w-full h-56 object-cover hover:scale-105 transition-transform duration-300" 
              />
              <CardContent className="p-4">
                <h2 className="text-2xl font-semibold text-blue-800 mb-2">{park.name}</h2>
                <p className="text-gray-700 mb-3 flex items-center">
                  <span className="mr-2">📍</span>
                  {park.location}
                </p>
                <div className="flex flex-wrap gap-2">
                  {park.features.map((feature, i) => (
                    <Badge key={i} className="bg-blue-200 text-blue-800 hover:bg-blue-300 transition-colors">
                      {feature}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        
        <div className="mt-12 text-center">
          <p className="text-blue-700 text-sm">
            🐕‍🦺 All dog parks are off-leash areas. Please follow local regulations and clean up after your pets!
          </p>
        </div>
      </div>
    </div>
  );
} 