import React, { useState, useEffect, useRef } from 'react';
import { Ambulance, Hospital, Activity, LogOut, Clock, MapPin, ChevronRight, Phone, Heart, Zap, Shield, Users, X } from 'lucide-react';

// Components
import EmerzoMap from './components/EmerzoMap';
import SOSButton from './components/SOSButton';
import StatusCard from './components/StatusCard';

// API Functions
import { triggerEmergency, fetchHospitalRequests, acceptRequest } from './services/api';

function App() {
  const [userType, setUserType] = useState(null);
  const [location, setLocation] = useState({ lat: null, lng: null });
  const [emergencyStatus, setEmergencyStatus] = useState('IDLE');
  const [assignedHospital, setAssignedHospital] = useState(null);
  const [incomingRequests, setIncomingRequests] = useState([]);

  // Auth States
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState('signin');

  // --- 1. REF FOR SCROLLING ---
  const servicesRef = useRef(null);

  const scrollToServices = () => {
    servicesRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // --- 2. PATIENT LOCATION ---
  useEffect(() => {
    if (userType === 'patient') {
      setLocation({ lat: 23.8480, lng: 78.7950 });
    }
  }, [userType]);

  // --- 3. HOSPITAL POLLING ---
  useEffect(() => {
    let interval;
    if (userType === 'hospital') {
      interval = setInterval(async () => {
        const data = await fetchHospitalRequests();
        if (data) setIncomingRequests(data);
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [userType]);

  // --- ACTIONS ---
  const handleSOSClick = async () => {
    if (!location.lat) return alert("Waiting for GPS...");
    setEmergencyStatus('LOADING');
    try {
      const data = await triggerEmergency(location.lat, location.lng);
      setAssignedHospital({
        name: data.hospital,
        lat: data.hospital_lat,
        lng: data.hospital_lng,
        distance: data.distance_km
      });
      setEmergencyStatus('ACTIVE');
    } catch (error) {
      alert("Error: Backend not reachable.");
      setEmergencyStatus('IDLE');
    }
  };

  const handleAccept = async (id) => {
    try {
      await acceptRequest(id);
      alert("✅ Mission Started! Ambulance Dispatched.");
      setIncomingRequests(prev => prev.filter(req => req.id !== id));
    } catch (err) {
      alert("Error accepting request.");
    }
  };

  const handleLoginSubmit = (e) => {
    e.preventDefault();
    setShowAuthModal(false);
    setUserType('patient'); 
  };

  // --- AUTH MODAL COMPONENT ---
  const AuthModal = () => (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/80 backdrop-blur-sm" onClick={() => setShowAuthModal(false)}></div>
      <div className="relative w-full max-w-md bg-[#0b0f19] border border-white/5 rounded-2xl shadow-2xl overflow-hidden flex flex-col" style={{ maxHeight: '90vh' }}>
        <button onClick={() => setShowAuthModal(false)} className="absolute top-4 right-4 text-slate-400 hover:text-white z-20">
          <X size={20} />
        </button>

        {authMode === 'signin' ? (
          <div className="p-8">
            <h2 className="text-2xl font-bold mb-6">User Sign In</h2>
            <form onSubmit={handleLoginSubmit} className="space-y-5">
              <div>
                <label className="block text-slate-400 text-xs mb-1.5 ml-1">Email</label>
                <input type="email" required className="w-full bg-[#131316] border border-white/5 rounded-lg px-4 py-3 focus:outline-none focus:border-red-500 transition text-sm text-white" placeholder="Enter your email" />
              </div>
              <div>
                <label className="block text-slate-400 text-xs mb-1.5 ml-1">Password</label>
                <input type="password" required className="w-full bg-[#131316] border border-white/5 rounded-lg px-4 py-3 focus:outline-none focus:border-red-500 transition text-sm text-white" placeholder="Enter your password" />
              </div>
              <button type="submit" className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 rounded-lg shadow-lg shadow-red-900/20 transition">
                Sign In
              </button>
            </form>
            <p className="text-center text-slate-500 text-sm mt-6">
              Don't have an account? <button onClick={() => setAuthMode('signup')} className="text-red-500 font-bold ml-1">Sign Up</button>
            </p>
          </div>
        ) : (
          <div className="flex flex-col h-full">
            <div className="p-6 border-b border-white/5 shrink-0 text-white">
              <h2 className="text-xl font-bold">Create Account</h2>
            </div>
            <div className="p-8 overflow-y-auto flex-1 custom-scrollbar space-y-4">
              <form onSubmit={handleLoginSubmit} className="space-y-4">
                <div>
                  <label className="block text-slate-400 text-xs mb-1 font-semibold">Full Name</label>
                  <input type="text" required className="w-full bg-[#131316] border border-white/5 rounded-lg px-4 py-3 text-sm text-white" placeholder="Enter your full name" />
                </div>
                <div>
                  <label className="block text-slate-400 text-xs mb-1 font-semibold">Email</label>
                  <input type="email" required className="w-full bg-[#131316] border border-white/5 rounded-lg px-4 py-3 text-sm text-white" placeholder="Enter your email" />
                </div>
                <div>
                  <label className="block text-slate-400 text-xs mb-1 font-semibold">Phone Number</label>
                  <input type="tel" required className="w-full bg-[#131316] border border-white/5 rounded-lg px-4 py-3 text-sm text-white" placeholder="Enter phone number" />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-slate-400 text-xs mb-1 font-semibold">DOB</label>
                    <input type="date" required className="w-full bg-[#131316] border border-white/5 rounded-lg px-4 py-3 text-sm text-slate-400" />
                  </div>
                  <div>
                    <label className="block text-slate-400 text-xs mb-1 font-semibold">Blood Group</label>
                    <select className="w-full bg-[#131316] border border-white/5 rounded-lg px-4 py-3 text-sm text-slate-400">
                      <option>Select</option><option>A+</option><option>B+</option><option>O+</option><option>AB+</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label className="block text-slate-400 text-xs mb-1 font-semibold">Password</label>
                  <input type="password" required className="w-full bg-[#131316] border border-white/5 rounded-lg px-4 py-3 text-sm text-white" placeholder="Min 8 characters" />
                </div>
                <div className="flex items-start gap-2 pt-2">
                  <input type="checkbox" required className="mt-1 rounded bg-[#131316] border-white/5 text-red-600" />
                  <p className="text-[11px] text-slate-500 leading-tight">I agree to share my location for emergency services and accept terms.</p>
                </div>
                <button type="submit" className="w-full bg-red-600 text-white font-bold py-3 rounded-lg shadow-lg mt-2">Sign Up</button>
              </form>
              <p className="text-center text-slate-500 text-xs mt-4 pb-4">
                Already have an account? <button onClick={() => setAuthMode('signin')} className="text-red-500 font-bold ml-1">Sign In</button>
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  // --- SCREEN 1: LANDING PAGE ---
  if (!userType) {
    return (
      <div className="min-h-screen bg-[#0B0B0F] text-white font-sans selection:bg-red-500/30 overflow-x-hidden">
        <nav className="flex justify-between items-center p-6 max-w-7xl mx-auto w-full">
          <div className="flex items-center gap-3">
            <div className="bg-red-500/10 p-2 rounded-lg border border-red-500/20">
              <div className="bg-red-600 rounded w-6 h-6 flex items-center justify-center text-white font-bold text-lg">+</div>
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-wide">Emerzo</h1>
              <p className="text-[10px] text-red-400 uppercase tracking-widest opacity-80">Every second matters</p>
            </div>
          </div>
          <div className="flex gap-4">
            <button 
              onClick={() => { setAuthMode('signin'); setShowAuthModal(true); }}
              className="bg-red-600 hover:bg-red-700 text-white px-5 py-2 rounded-lg text-sm font-semibold transition shadow-[0_0_15px_rgba(220,38,38,0.5)]"
            >
              User Sign In
            </button>
            <button 
              onClick={() => setUserType('hospital')}
              className="border border-white/10 hover:bg-white/5 text-slate-300 px-5 py-2 rounded-lg text-sm font-semibold transition"
            >
              Hospital Portal
            </button>
          </div>
        </nav>

        <div className="flex flex-col items-center justify-center text-center mt-12 px-4 relative">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-red-600/10 rounded-full blur-[120px] pointer-events-none"></div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-red-500/30 bg-red-500/10 text-red-400 text-xs font-semibold mb-6">
            <div className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse"></div>
            24/7 Emergency Support
          </div>

          <h1 className="text-5xl md:text-7xl font-bold mb-6 tracking-tight z-10">
            Emerzo <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-b from-white to-slate-400">When You Need It</span>
          </h1>

          <p className="text-slate-400 text-lg max-w-2xl mb-10 z-10">
            Access immediate medical assistance, locate nearby hospitals, and get expert health guidance—all in one place
          </p>

          {/* CALL AMBULANCE NOW: Opens the Map directly */}
          <button 
            onClick={() => setUserType('patient')}
            className="w-full max-w-xl bg-gradient-to-r from-red-700 to-red-600 p-1 rounded-xl shadow-[0_0_40px_rgba(220,38,38,0.3)] hover:scale-[1.02] transition-transform z-10 group cursor-pointer"
          >
            <div className="bg-[#1a0f0f] rounded-lg px-8 py-4 flex items-center justify-center gap-3">
              <Zap className="text-red-500 fill-red-500" size={24} />
              <span className="text-xl font-bold tracking-wider">CALL AMBULANCE NOW</span>
              <Zap className="text-red-500 fill-red-500" size={24} />
            </div>
          </button>
          <p className="text-slate-500 text-xs mt-3 mb-8 z-10">Instantly dispatches ambulance to your GPS location</p>

          {/* GET HELP NOW: Scrolls to Services */}
          <button 
             onClick={scrollToServices}
             className="bg-red-600 hover:bg-red-700 px-8 py-3 rounded-lg font-bold shadow-lg z-10 transition"
          >
            Get Help Now
          </button>
        </div>

        {showAuthModal && <AuthModal />}

        <div className="max-w-7xl mx-auto px-6 mt-24 mb-20">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Partner Hospitals", val: "Beta Testing" },
              { label: "System Target", val: "<3min" },
              { label: "Users Helped", val: "System Live" },
              { label: "Available", val: "24/7" },
            ].map((stat, i) => (
              <div key={i} className="bg-[#131316] border border-white/5 p-6 rounded-2xl text-center hover:border-red-500/30 transition duration-300">
                <h3 className="text-3xl font-bold text-red-500 mb-1">{stat.val}</h3>
                <p className="text-slate-400 text-sm">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>

        {/* SERVICES SECTION WITH REF */}
        <div ref={servicesRef} className="max-w-7xl mx-auto px-6 mb-24">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-3">Our Services</h2>
            <p className="text-slate-400">Comprehensive emergency healthcare solutions at your fingertips</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
             <div onClick={() => setUserType('patient')} className="bg-[#131316] p-8 rounded-2xl border border-white/5 hover:border-red-500/50 transition cursor-pointer group">
                <div className="bg-[#1F1212] w-12 h-12 rounded-xl flex items-center justify-center mb-6 group-hover:bg-red-600 transition-colors">
                  <Phone className="text-red-500 group-hover:text-white" size={24} />
                </div>
                <h3 className="text-xl font-bold mb-2">Emergency Call</h3>
                <p className="text-slate-400 text-sm leading-relaxed">Instantly connect with emergency services and get immediate help</p>
             </div>

             <div onClick={() => setUserType('patient')} className="bg-[#131316] p-8 rounded-2xl border border-white/5 hover:border-red-500/50 transition cursor-pointer group">
                <div className="bg-[#1F1212] w-12 h-12 rounded-xl flex items-center justify-center mb-6 group-hover:bg-red-600 transition-colors">
                  <MapPin className="text-red-500 group-hover:text-white" size={24} />
                </div>
                <h3 className="text-xl font-bold mb-2">Find Hospitals</h3>
                <p className="text-slate-400 text-sm leading-relaxed">Locate nearby hospitals with real-time availability info</p>
             </div>

             <div className="bg-[#131316] p-8 rounded-2xl border border-white/5 hover:border-red-500/50 transition cursor-pointer group">
                <div className="bg-[#1F1212] w-12 h-12 rounded-xl flex items-center justify-center mb-6 group-hover:bg-red-600 transition-colors">
                  <Activity className="text-red-500 group-hover:text-white" size={24} />
                </div>
                <h3 className="text-xl font-bold mb-2">AI Assistant</h3>
                <p className="text-slate-400 text-sm leading-relaxed">Get instant health guidance from our AI-powered assistant</p>
             </div>

             <div className="bg-[#131316] p-8 rounded-2xl border border-white/5 hover:border-red-500/50 transition cursor-pointer group">
                <div className="bg-[#1F1212] w-12 h-12 rounded-xl flex items-center justify-center mb-6 group-hover:bg-red-600 transition-colors">
                  <Heart className="text-red-500 group-hover:text-white" size={24} />
                </div>
                <h3 className="text-xl font-bold mb-2">First Aid Guide</h3>
                <p className="text-slate-400 text-sm leading-relaxed">Step-by-step first aid instructions for common emergencies</p>
             </div>
          </div>
        </div>
      </div>
    );
  }

  // --- SCREEN 2: PATIENT DASHBOARD (MAP) ---
  if (userType === 'patient') {
    const mapMarkers = assignedHospital ? [{ lat: assignedHospital.lat, lng: assignedHospital.lng, name: assignedHospital.name }] : [];
    return (
      <div className="min-h-screen bg-[#0B0B0F] flex flex-col relative overflow-hidden">
        <header className="absolute top-6 left-6 right-6 z-20">
          <div className="bg-[#131316]/90 backdrop-blur-md shadow-2xl rounded-2xl px-6 py-4 flex justify-between items-center border border-white/10">
            <h1 className="text-xl font-bold text-white flex items-center gap-3">
              <span className="bg-red-600 p-1.5 rounded text-white">+</span> Emerzo
            </h1>
            <button onClick={() => setUserType(null)} className="p-2 hover:bg-white/5 rounded-full text-slate-400 hover:text-red-500 transition">
              <LogOut size={20}/>
            </button>
          </div>
        </header>
        
        <div className="absolute inset-0 z-0">
          <EmerzoMap lat={location.lat} lng={location.lng} hospitals={mapMarkers} />
        </div>
        
        <div className="absolute bottom-0 left-0 right-0 z-10 p-6 flex justify-center pb-10 bg-gradient-to-t from-black via-black/90 to-transparent pointer-events-none">
          <div className="pointer-events-auto w-full max-w-md">
            {emergencyStatus === 'ACTIVE' ? (
              <StatusCard status="Dispatched" hospitalName={assignedHospital?.name} distance={assignedHospital?.distance} />
            ) : (
              <SOSButton onClick={handleSOSClick} isLoading={emergencyStatus === 'LOADING'} />
            )}
          </div>
        </div>
      </div>
    );
  }

  // --- SCREEN 3: HOSPITAL DASHBOARD ---
  if (userType === 'hospital') {
    return (
      <div className="min-h-screen bg-[#0B0B0F] flex flex-col font-sans text-white">
        <header className="bg-[#131316] border-b border-white/5 z-20">
          <div className="max-w-7xl mx-auto px-8 py-5 flex justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="bg-red-600/10 p-2 rounded-lg border border-red-600/20"><Hospital className="text-red-500" size={24} /></div>
              <div>
                <h1 className="font-bold text-xl">Dr. Rai Hospital</h1>
                <div className="flex items-center gap-2 mt-0.5">
                  <div className="h-1.5 w-1.5 rounded-full bg-green-500 animate-pulse"></div>
                  <p className="text-[10px] text-slate-400 uppercase tracking-widest">System Live</p>
                </div>
              </div>
            </div>
            <button onClick={() => setUserType(null)} className="px-5 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm font-semibold transition border border-white/5">Sign Out</button>
          </div>
        </header>

        <main className="flex-1 max-w-7xl mx-auto w-full p-8">
          <div className="flex justify-between items-center mb-10">
            <div>
               <h2 className="text-2xl font-bold">Incoming Requests</h2>
               <p className="text-slate-500 text-sm mt-1">Real-time emergency dispatch console</p>
            </div>
            {incomingRequests.length > 0 && (
              <div className="bg-red-600 text-white px-4 py-1.5 rounded-full text-sm font-bold flex gap-2 animate-pulse shadow-lg shadow-red-900/40">
                <Activity size={18} /> {incomingRequests.length} ACTIVE
              </div>
            )}
          </div>

          <div className="space-y-4">
            {incomingRequests.length === 0 ? (
              <div className="p-20 bg-[#131316] rounded-2xl border border-white/5 text-center border-dashed">
                <Shield size={48} className="mx-auto text-slate-700 mb-4"/>
                <h3 className="text-slate-300 font-medium">No Active Alerts</h3>
                <p className="text-slate-600 text-sm mt-1">Monitoring network...</p>
              </div>
            ) : (
              incomingRequests.map((req) => (
                <div key={req.id} className="bg-[#131316] rounded-xl border-l-4 border-red-600 p-6 flex flex-col md:flex-row justify-between items-center shadow-lg hover:bg-[#18181b] transition-colors">
                  <div className="flex items-center gap-5 mb-4 md:mb-0">
                    <div className="bg-red-500/10 p-4 rounded-full"><Activity className="text-red-500" size={24} /></div>
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                         <h3 className="font-bold text-lg text-white">SOS: {req.patient_id}</h3>
                         <span className="bg-red-500/20 text-red-400 text-[10px] px-2 py-0.5 rounded uppercase font-bold tracking-wider">Critical</span>
                      </div>
                      <div className="flex gap-4 text-sm text-slate-400">
                        <span className="flex items-center gap-1"><MapPin size={14}/> {req.distance} km</span>
                        <span className="flex items-center gap-1"><Clock size={14}/> {req.time}</span>
                      </div>
                    </div>
                  </div>
                  <button 
                    onClick={() => handleAccept(req.id)} 
                    className="bg-red-600 hover:bg-red-700 text-white px-8 py-3 rounded-lg font-bold shadow-lg shadow-red-900/30 transition-all active:scale-95"
                  >
                    DISPATCH UNIT
                  </button>
                </div>
              ))
            )}
          </div>
        </main>
      </div>
    );
  }
}

export default App;