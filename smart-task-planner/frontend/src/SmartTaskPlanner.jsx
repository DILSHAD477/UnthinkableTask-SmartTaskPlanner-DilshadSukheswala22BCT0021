import { AlertTriangle, ArrowRight, Award, Calendar, CheckCircle, Clock, GitBranch, Layers, Menu, Play, Rocket, Shield, Sparkles, Star, Target, TrendingUp, Users, X, Zap } from 'lucide-react';
import { useEffect, useState } from 'react';

const SmartTaskPlanner = () => {
  const [goal, setGoal] = useState('');
  const [deadline, setDeadline] = useState('');
  const [context, setContext] = useState('');
  const [domain, setDomain] = useState('general');
  const [resources, setResources] = useState('');
  const [workingHours, setWorkingHours] = useState(8);
  const [plan, setPlan] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [activeView, setActiveView] = useState('home');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [showFeatures, setShowFeatures] = useState(false);
  const [showAbout, setShowAbout] = useState(false);

  const domains = [
    { value: 'general', label: 'General' },
    { value: 'business', label: 'Business' },
    { value: 'technical', label: 'Technical' },
    { value: 'personal', label: 'Personal' },
    { value: 'academic', label: 'Academic' },
    { value: 'creative', label: 'Creative' }
  ];

  const priorityColors = {
    critical: 'bg-purple-100 text-purple-900 border-purple-300',
    high: 'bg-purple-50 text-purple-800 border-purple-200',
    medium: 'bg-purple-25 text-purple-700 border-purple-150',
    low: 'bg-gray-50 text-purple-600 border-purple-100'
  };

  const riskColors = {
    high: 'text-purple-700',
    medium: 'text-purple-600',
    low: 'text-purple-500',
    unknown: 'text-gray-600'
  };

  // Generate random floating blocks
  const [floatingBlocks, setFloatingBlocks] = useState([]);
  
  useEffect(() => {
    const generateBlocks = () => {
      const blocks = [];
      for (let i = 0; i < 15; i++) {
        blocks.push({
          id: i,
          size: Math.random() * 20 + 10,
          x: Math.random() * 100,
          y: Math.random() * 100,
          opacity: Math.random() * 0.3 + 0.1,
          duration: Math.random() * 20 + 10,
          delay: Math.random() * 10
        });
      }
      setFloatingBlocks(blocks);
    };
    generateBlocks();
  }, [activeView]);

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!goal.trim()) return;
    setIsLoading(true);

    const goalInput = {
      goal,
      deadline: deadline ? new Date(deadline).toISOString() : null,
      context: context || null,
      domain,
      resources: resources ? resources.split(',').map(r => r.trim()) : [],
      working_hours_per_day: workingHours
    };

    try {
      const response = await fetch('/api/create-plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(goalInput)
      });

      if (response.ok) {
        const planData = await response.json();
        setPlan(planData);
        setActiveView('tasks');
      } else {
        throw new Error('API call failed');
      }
    } catch (error) {
      console.error('Error creating plan:', error);
      alert('Failed to create plan. Please check if the backend is running on http://localhost:8000');
    }

    setIsLoading(false);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const getConfidenceColor = (score) => {
    if (score >= 0.8) return 'text-purple-600';
    if (score >= 0.6) return 'text-purple-500';
    return 'text-purple-400';
  };

  const TaskCard = ({ task, index }) => (
    <div className="group bg-white/70 backdrop-blur-sm rounded-xl border border-purple-200 p-4 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.01] hover:bg-white/80 animate-fadeInUp" style={{ animationDelay: `${index * 100}ms` }}>
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-6 h-6 rounded-full bg-gradient-to-r from-purple-500 to-purple-600 flex items-center justify-center text-white font-bold text-xs group-hover:scale-110 transition-transform">
              {index + 1}
            </div>
            <span className={`px-2 py-1 rounded-full text-xs font-medium border ${priorityColors[task.priority]} group-hover:scale-105 transition-transform`}>
              {task.priority.toUpperCase()}
            </span>
          </div>
          <h3 className="text-lg font-bold text-purple-900 mb-2 group-hover:text-purple-800 transition-colors">{task.title}</h3>
          <p className="text-gray-700 mb-3 text-sm leading-relaxed">{task.description}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-3">
        <div className="flex items-center gap-2 p-2 bg-purple-50 rounded-lg">
          <Clock className="h-4 w-4 text-purple-600" />
          <span className="text-xs font-medium text-gray-700">{task.estimated_hours}h estimated</span>
        </div>
        <div className="flex items-center gap-2 p-2 bg-purple-50 rounded-lg">
          <TrendingUp className="h-4 w-4 text-purple-600" />
          <span className={`text-xs font-bold ${getConfidenceColor(task.confidence_score)}`}>
            {Math.round(task.confidence_score * 100)}% confidence
          </span>
        </div>
      </div>

      {task.start_date && task.end_date && (
        <div className="flex items-center gap-2 mb-3 p-2 bg-gradient-to-r from-purple-50 to-purple-25 rounded-lg">
          <Calendar className="h-4 w-4 text-purple-600" />
          <span className="text-xs font-medium text-gray-700">
            {formatDate(task.start_date)} → {formatDate(task.end_date)}
          </span>
        </div>
      )}

      {task.dependencies && task.dependencies.length > 0 && (
        <div className="mb-3">
          <div className="flex items-center gap-2 mb-1">
            <GitBranch className="h-4 w-4 text-purple-600" />
            <span className="text-xs font-bold text-gray-800">Dependencies:</span>
          </div>
          <div className="flex flex-wrap gap-1">
            {task.dependencies.map((dep, idx) => (
              <span key={idx} className="px-2 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-medium border border-purple-200">
                {dep}
              </span>
            ))}
          </div>
        </div>
      )}

      {task.risk_factors && task.risk_factors.length > 0 && (
        <div className="mb-3">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="h-4 w-4 text-purple-600" />
            <span className="text-xs font-bold text-gray-800">Risk Factors:</span>
          </div>
          <ul className="space-y-1">
            {task.risk_factors.map((risk, idx) => (
              <li key={idx} className="text-xs text-purple-700 pl-3 py-1 border-l-2 border-purple-300 bg-purple-25">
                • {risk}
              </li>
            ))}
          </ul>
        </div>
      )}

      {task.success_criteria && task.success_criteria.length > 0 && (
        <div className="mb-3">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="h-4 w-4 text-purple-600" />
            <span className="text-xs font-bold text-gray-800">Success Criteria:</span>
          </div>
          <ul className="space-y-1">
            {task.success_criteria.map((criterion, idx) => (
              <li key={idx} className="text-xs text-purple-700 pl-3 py-1 border-l-2 border-purple-300 bg-purple-25">
                ✓ {criterion}
              </li>
            ))}
          </ul>
        </div>
      )}

      {task.resources_needed && task.resources_needed.length > 0 && (
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Users className="h-4 w-4 text-purple-600" />
            <span className="text-xs font-bold text-gray-800">Resources Needed:</span>
          </div>
          <div className="flex flex-wrap gap-1">
            {task.resources_needed.map((resource, idx) => (
              <span key={idx} className="px-2 py-1 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-full text-xs font-medium shadow-md">
                {resource}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  const FloatingBlocks = () => (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      {floatingBlocks.map((block) => (
        <div
          key={block.id}
          className="absolute bg-gradient-to-r from-purple-300/20 to-purple-400/20 rounded-lg animate-float"
          style={{
            width: `${block.size}px`,
            height: `${block.size}px`,
            left: `${block.x}%`,
            top: `${block.y}%`,
            opacity: block.opacity,
            animationDuration: `${block.duration}s`,
            animationDelay: `${block.delay}s`,
          }}
        />
      ))}
    </div>
  );

  const FeatureModal = () => (
    showFeatures && (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div className="bg-white/90 backdrop-blur-sm rounded-2xl max-w-2xl w-full p-6 max-h-[80vh] overflow-y-auto animate-fadeInUp">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-purple-900">Features</h2>
            <button onClick={() => setShowFeatures(false)} className="p-2 hover:bg-purple-100 rounded-full">
              <X className="h-5 w-5 text-purple-600" />
            </button>
          </div>
          <div className="space-y-4">
            {[
              {
                icon: <Rocket className="h-5 w-5 text-purple-600" />,
                title: "AI-Powered Task Generation",
                description: "Advanced machine learning algorithms analyze your goals and automatically generate comprehensive task breakdowns"
              },
              {
                icon: <Shield className="h-5 w-5 text-purple-600" />,
                title: "Risk Assessment & Mitigation",
                description: "Proactively identify potential roadblocks and get intelligent suggestions for risk mitigation strategies"
              },
              {
                icon: <Award className="h-5 w-5 text-purple-600" />,
                title: "Timeline Optimization",
                description: "Smart scheduling based on dependencies, resource availability, and critical path analysis"
              }
            ].map((feature, index) => (
              <div key={index} className="flex gap-3 p-3 bg-purple-50 rounded-lg">
                <div className="flex-shrink-0">{feature.icon}</div>
                <div>
                  <h3 className="font-bold text-purple-900 text-sm mb-1">{feature.title}</h3>
                  <p className="text-gray-700 text-xs">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  );

  const AboutModal = () => (
    showAbout && (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div className="bg-white/90 backdrop-blur-sm rounded-2xl max-w-2xl w-full p-6 max-h-[80vh] overflow-y-auto animate-fadeInUp">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-purple-900">About SmartPlan AI</h2>
            <button onClick={() => setShowAbout(false)} className="p-2 hover:bg-purple-100 rounded-full">
              <X className="h-5 w-5 text-purple-600" />
            </button>
          </div>
          <div className="space-y-4">
            <p className="text-gray-700 text-sm leading-relaxed">
              SmartPlan AI revolutionizes project planning by combining artificial intelligence with proven project management methodologies. Our platform transforms your high-level goals into actionable, time-bound tasks with intelligent risk assessment and resource optimization.
            </p>
            <div className="bg-purple-50 p-4 rounded-lg">
              <h3 className="font-bold text-purple-900 text-sm mb-2">Mission</h3>
              <p className="text-gray-700 text-xs">
                To democratize intelligent project planning and help individuals and teams achieve their goals more efficiently through AI-powered insights.
              </p>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <h3 className="font-bold text-purple-900 text-sm mb-2">Technology</h3>
              <p className="text-gray-700 text-xs">
                Built with FastAPI backend, React frontend, and powered by advanced algorithms for dependency analysis, timeline optimization, and risk assessment.
              </p>
            </div>
          </div>
        </div>
      </div>
    )
  );

  if (activeView === 'home') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-200 via-purple-100 to-white relative overflow-hidden">
        <FloatingBlocks />
        
        {/* Header */}
        <header className="relative z-10 px-4 py-6">
          <nav className="max-w-6xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-2 animate-fadeInLeft">
              <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-purple-700 rounded-xl flex items-center justify-center shadow-lg">
                <Sparkles className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-purple-700 to-purple-500 bg-clip-text text-transparent">
                SmartPlan AI
              </span>
            </div>
            
            {/* Desktop Menu */}
            <div className="hidden md:flex items-center gap-4 animate-fadeInRight">
              <button 
                onClick={() => setShowFeatures(true)}
                className="text-gray-700 hover:text-purple-600 font-medium transition-colors text-sm"
              >
                Features
              </button>
              <button 
                onClick={() => setShowAbout(true)}
                className="text-gray-700 hover:text-purple-600 font-medium transition-colors text-sm"
              >
                About
              </button>
              <button className="px-4 py-2 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all duration-300 hover:scale-105 text-sm">
                Sign In
              </button>
            </div>

            {/* Mobile Menu Button */}
            <button 
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 text-purple-600"
            >
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </nav>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="md:hidden absolute top-full left-0 right-0 bg-white/90 backdrop-blur-sm border-b border-purple-200 shadow-lg animate-fadeInUp">
              <div className="px-4 py-4 space-y-2">
                <button 
                  onClick={() => { setShowFeatures(true); setMobileMenuOpen(false); }}
                  className="block w-full text-left text-gray-700 hover:text-purple-600 font-medium py-2 text-sm"
                >
                  Features
                </button>
                <button 
                  onClick={() => { setShowAbout(true); setMobileMenuOpen(false); }}
                  className="block w-full text-left text-gray-700 hover:text-purple-600 font-medium py-2 text-sm"
                >
                  About
                </button>
                <button className="w-full px-4 py-2 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg text-sm">
                  Sign In
                </button>
              </div>
            </div>
          )}
        </header>

        {/* Hero Section */}
        <section className="relative z-10 px-4 py-16">
          <div className="max-w-6xl mx-auto text-center">
            <div className="animate-fadeInUp">
              <h1 className="text-4xl md:text-5xl font-bold text-purple-900 mb-4 leading-tight">
                Turn Your{' '}
                <span className="bg-gradient-to-r from-purple-600 to-purple-800 bg-clip-text text-transparent">
                  Goals
                </span>
                <br />
                Into{' '}
                <span className="bg-gradient-to-r from-purple-600 to-purple-800 bg-clip-text text-transparent">
                  Smart Plans
                </span>
              </h1>
              <p className="text-lg text-gray-600 mb-6 max-w-2xl mx-auto leading-relaxed">
                AI-powered task planning that breaks down your biggest goals into actionable steps with intelligent timeline optimization and risk assessment
              </p>
              <button
                onClick={() => setActiveView('planner')}
                className="group inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-purple-700 text-white font-semibold rounded-xl shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 animate-bounce text-sm"
                style={{ animationDuration: '2s' }}
              >
                <Play className="h-5 w-5 group-hover:scale-110 transition-transform" />
                Start Planning Now
                <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="relative z-10 px-4 py-16 bg-white/40 backdrop-blur-sm">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12 animate-fadeInUp">
              <h2 className="text-3xl font-bold text-purple-900 mb-3">
                Why Choose{' '}
                <span className="bg-gradient-to-r from-purple-600 to-purple-800 bg-clip-text text-transparent">
                  SmartPlan AI?
                </span>
              </h2>
              <p className="text-lg text-gray-600 max-w-xl mx-auto">
                Experience the future of project planning with our intelligent AI assistant
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[
                {
                  icon: <Zap className="h-6 w-6 text-purple-600" />,
                  title: "AI-Powered Intelligence",
                  description: "Advanced algorithms analyze your goals and create optimized task breakdowns with realistic timelines"
                },
                {
                  icon: <Target className="h-6 w-6 text-purple-600" />,
                  title: "Smart Risk Assessment",
                  description: "Identify potential roadblocks before they happen with comprehensive risk analysis and mitigation strategies"
                },
                {
                  icon: <Star className="h-6 w-6 text-purple-600" />,
                  title: "Dynamic Optimization",
                  description: "Automatically optimize schedules based on dependencies, resources, and critical path analysis"
                }
              ].map((feature, index) => (
                <div key={index} className="group bg-white/70 backdrop-blur-sm rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 animate-fadeInUp" style={{ animationDelay: `${index * 200}ms` }}>
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-100 to-purple-200 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    {feature.icon}
                  </div>
                  <h3 className="text-lg font-bold text-purple-900 mb-3">{feature.title}</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="relative z-10 px-4 py-16">
          <div className="max-w-3xl mx-auto text-center">
            <div className="bg-gradient-to-r from-purple-600 to-purple-800 rounded-2xl p-8 shadow-2xl animate-fadeInUp">
              <h2 className="text-3xl font-bold text-white mb-4">
                Ready to Transform Your Planning?
              </h2>
              <p className="text-purple-100 mb-6 max-w-xl mx-auto">
                Join thousands of professionals who've revolutionized their productivity with SmartPlan AI
              </p>
              <button
                onClick={() => setActiveView('planner')}
                className="inline-flex items-center gap-2 px-6 py-3 bg-white text-purple-700 font-bold rounded-xl hover:bg-purple-50 transition-all duration-300 hover:scale-105 shadow-lg text-sm"
              >
                <Sparkles className="h-5 w-5" />
                Create Your First Smart Plan
                <ArrowRight className="h-5 w-5" />
              </button>
            </div>
          </div>
        </section>

        <FeatureModal />
        <AboutModal />
      </div>
    );
  }

  if (activeView === 'planner') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-200 via-purple-100 to-white relative overflow-hidden">
        <FloatingBlocks />

        <div className="max-w-4xl mx-auto px-4 py-8 relative z-10">
          {/* Header */}
          <div className="text-center mb-8 animate-fadeInUp">
            <button
              onClick={() => setActiveView('home')}
              className="inline-flex items-center gap-1 text-purple-600 hover:text-purple-700 font-medium mb-4 transition-colors text-sm"
            >
              ← Back to Home
            </button>
            <h1 className="text-4xl font-bold text-purple-900 mb-3">
              Create Your{' '}
              <span className="bg-gradient-to-r from-purple-600 to-purple-800 bg-clip-text text-transparent">
                Smart Plan
              </span>
            </h1>
            <p className="text-lg text-gray-600 max-w-xl mx-auto">
              Tell us about your goal and watch AI create a detailed, optimized plan in seconds
            </p>
          </div>

          {/* Planning Form */}
          <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-purple-200 animate-fadeInUp" style={{ animationDelay: '200ms' }}>
            <div className="p-6 space-y-6">
              <div className="space-y-1">
                <label className="block text-sm font-bold text-purple-900">
                  What's your goal? *
                </label>
                <textarea
                  value={goal}
                  onChange={(e) => setGoal(e.target.value)}
                  placeholder="e.g., Launch a mobile app in 3 months, Learn machine learning, Organize a conference..."
                  className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-100 focus:border-purple-400 resize-none transition-all duration-300 bg-white/80 text-sm"
                  rows={3}
                  required
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="block text-sm font-bold text-purple-900">
                    Target Deadline (Optional)
                  </label>
                  <input
                    type="date"
                    value={deadline}
                    onChange={(e) => setDeadline(e.target.value)}
                    className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-100 focus:border-purple-400 transition-all duration-300 bg-white/80 text-sm"
                  />
                </div>

                <div className="space-y-1">
                  <label className="block text-sm font-bold text-purple-900">
                    Domain/Category
                  </label>
                  <select
                    value={domain}
                    onChange={(e) => setDomain(e.target.value)}
                    className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-100 focus:border-purple-400 transition-all duration-300 bg-white/80 text-sm"
                  >
                    {domains.map(d => (
                      <option key={d.value} value={d.value}>{d.label}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="space-y-1">
                <label className="block text-sm font-bold text-purple-900">
                  Additional Context (Optional)
                </label>
                <textarea
                  value={context}
                  onChange={(e) => setContext(e.target.value)}
                  placeholder="Any constraints, preferences, or additional information..."
                  className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-100 focus:border-purple-400 resize-none transition-all duration-300 bg-white/80 text-sm"
                  rows={2}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="block text-sm font-bold text-purple-900">
                    Available Resources (Optional)
                  </label>
                  <input
                    type="text"
                    value={resources}
                    onChange={(e) => setResources(e.target.value)}
                    placeholder="e.g., John (developer), Sarah (designer), Budget: $5000"
                    className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-100 focus:border-purple-400 transition-all duration-300 bg-white/80 text-sm"
                  />
                </div>

                <div className="space-y-1">
                  <label className="block text-sm font-bold text-purple-900">
                    Working Hours per Day
                  </label>
                  <input
                    type="number"
                    value={workingHours}
                    onChange={(e) => setWorkingHours(Number(e.target.value))}
                    min="1"
                    max="24"
                    className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-100 focus:border-purple-400 transition-all duration-300 bg-white/80 text-sm"
                  />
                </div>
              </div>

              <div className="pt-2">
                <button
                  type="button"
                  onClick={handleSubmit}
                  disabled={!goal.trim() || isLoading}
                  className="group w-full bg-gradient-to-r from-purple-600 to-purple-700 text-white py-4 px-6 rounded-xl hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 hover:scale-[1.01] font-bold text-sm"
                >
                  {isLoading ? (
                    <div className="flex items-center justify-center gap-2">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      AI is Creating Your Smart Plan...
                    </div>
                  ) : (
                    <div className="flex items-center justify-center gap-2">
                      <Sparkles className="h-5 w-5 group-hover:scale-110 transition-transform" />
                      Generate My Smart Plan
                      <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
                    </div>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-200 via-purple-100 to-white relative overflow-hidden">
      <FloatingBlocks />

      <div className="max-w-6xl mx-auto px-4 py-6 relative z-10">
        {/* Header */}
        <div className="mb-6 animate-fadeInUp">
          <button
            onClick={() => setActiveView('home')}
            className="inline-flex items-center gap-1 text-purple-600 hover:text-purple-700 font-medium mb-3 transition-colors text-sm"
          >
            ← Back to Home
          </button>
          
          <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-purple-200 p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h1 className="text-2xl font-bold text-purple-900 mb-1">{plan.goal}</h1>
                <p className="text-purple-600 font-medium text-sm">Plan ID: {plan.plan_id}</p>
              </div>
              <div className="text-right">
                <div className={`text-2xl font-bold ${getConfidenceColor(plan.confidence_score)}`}>
                  {Math.round(plan.confidence_score * 100)}%
                </div>
                <p className="text-xs text-gray-600 font-medium">Confidence Score</p>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl p-4 text-white transform hover:scale-105 transition-transform">
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4" />
                  <span className="font-bold text-sm">Total Hours</span>
                </div>
                <div className="text-xl font-bold mt-1">{plan.total_estimated_hours}</div>
              </div>
              
              <div className="bg-gradient-to-r from-purple-400 to-purple-500 rounded-xl p-4 text-white transform hover:scale-105 transition-transform">
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  <span className="font-bold text-sm">Duration</span>
                </div>
                <div className="text-xl font-bold mt-1">{plan.critical_path_duration} days</div>
              </div>
              
              <div className="bg-gradient-to-r from-purple-300 to-purple-400 rounded-xl p-4 text-white transform hover:scale-105 transition-transform">
                <div className="flex items-center gap-2">
                  <Layers className="h-4 w-4" />
                  <span className="font-bold text-sm">Tasks</span>
                </div>
                <div className="text-xl font-bold mt-1">{plan.tasks.length}</div>
              </div>
              
              <div className={`rounded-xl p-4 text-white transform hover:scale-105 transition-transform ${
                plan.risk_assessment.timeline_risk === 'high' ? 'bg-gradient-to-r from-purple-700 to-purple-800' : 
                plan.risk_assessment.timeline_risk === 'medium' ? 'bg-gradient-to-r from-purple-500 to-purple-600' : 
                'bg-gradient-to-r from-purple-300 to-purple-400'
              }`}>
                <div className="flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4" />
                  <span className="font-bold text-sm">Risk Level</span>
                </div>
                <div className="text-xl font-bold mt-1 capitalize">
                  {plan.risk_assessment.timeline_risk}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="mb-6 animate-fadeInUp" style={{ animationDelay: '100ms' }}>
          <div className="bg-white/70 backdrop-blur-sm rounded-xl shadow-lg border border-purple-200 p-1">
            <nav className="flex space-x-1">
              {['tasks', 'timeline', 'risks', 'recommendations'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveView(tab)}
                  className={`flex-1 py-2 px-4 rounded-lg font-bold text-xs capitalize transition-all duration-300 ${
                    activeView === tab
                      ? 'bg-gradient-to-r from-purple-500 to-purple-600 text-white shadow-lg'
                      : 'text-gray-600 hover:text-purple-600 hover:bg-purple-50'
                  }`}
                >
                  {tab}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Content Sections */}
        {activeView === 'tasks' && (
          <div className="space-y-6 animate-fadeInUp" style={{ animationDelay: '200ms' }}>
            <h2 className="text-2xl font-bold text-purple-900">Task Breakdown</h2>
            <div className="grid gap-6">
              {plan.tasks.map((task, index) => (
                <TaskCard key={task.id} task={task} index={index} />
              ))}
            </div>
          </div>
        )}

        {activeView === 'timeline' && (
          <div className="space-y-6 animate-fadeInUp" style={{ animationDelay: '200ms' }}>
            <h2 className="text-2xl font-bold text-purple-900">Timeline & Milestones</h2>
            <div className="bg-white/70 backdrop-blur-sm rounded-xl border border-purple-200 p-6 shadow-xl">
              <div className="space-y-4">
                {plan.milestones.map((milestone, index) => (
                  <div key={index} className="flex items-center gap-4 p-4 bg-gradient-to-r from-purple-50 to-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 animate-fadeInUp" style={{ animationDelay: `${index * 150}ms` }}>
                    <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                      <span className="text-white font-bold">{milestone.percentage}%</span>
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-purple-900 mb-1">{milestone.title}</h3>
                      <p className="text-gray-700 mb-1 text-sm">{milestone.description}</p>
                      <p className="text-xs text-purple-600 font-medium">Target: {formatDate(milestone.date)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeView === 'risks' && (
          <div className="space-y-6 animate-fadeInUp" style={{ animationDelay: '200ms' }}>
            <h2 className="text-2xl font-bold text-purple-900">Risk Assessment</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white/70 backdrop-blur-sm rounded-xl border border-purple-200 p-6 shadow-xl">
                <h3 className="text-lg font-bold text-purple-900 mb-4">Overall Risks</h3>
                <div className="space-y-3">
                  {Object.entries(plan.risk_assessment).map(([key, value], index) => (
                    <div key={key} className="flex justify-between items-center p-3 bg-purple-50 rounded-lg animate-fadeInUp" style={{ animationDelay: `${index * 100}ms` }}>
                      <span className="text-gray-700 font-medium capitalize text-sm">{key.replace('_', ' ')}</span>
                      <span className={`font-bold ${typeof value === 'string' ? riskColors[value] || '' : 'text-purple-600'} text-sm`}>
                        {typeof value === 'string' ? value.charAt(0).toUpperCase() + value.slice(1) : value}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="bg-white/70 backdrop-blur-sm rounded-xl border border-purple-200 p-6 shadow-xl">
                <h3 className="text-lg font-bold text-purple-900 mb-4">High-Risk Tasks</h3>
                <div className="space-y-3">
                  {plan.tasks
                    .filter(task => task.risk_factors && task.risk_factors.length > 1)
                    .map((task, index) => (
                      <div key={task.id} className="p-3 bg-gradient-to-r from-purple-100 to-purple-50 rounded-lg shadow-md animate-fadeInUp" style={{ animationDelay: `${index * 150}ms` }}>
                        <div className="font-bold text-purple-900 mb-1 text-sm">{task.title}</div>
                        <div className="text-xs text-purple-700 font-medium">
                          {task.risk_factors.length} risk factors identified
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeView === 'recommendations' && (
          <div className="space-y-6 animate-fadeInUp" style={{ animationDelay: '200ms' }}>
            <h2 className="text-2xl font-bold text-purple-900">AI Recommendations</h2>
            <div className="bg-white/70 backdrop-blur-sm rounded-xl border border-purple-200 p-6 shadow-xl">
              <div className="space-y-4">
                {plan.recommendations.map((recommendation, index) => (
                  <div key={index} className="flex gap-3 p-4 bg-gradient-to-r from-purple-50 to-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 animate-fadeInUp" style={{ animationDelay: `${index * 100}ms` }}>
                    <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg">
                      <span className="text-white font-bold text-xs">{index + 1}</span>
                    </div>
                    <p className="text-gray-800 font-medium leading-relaxed text-sm">{recommendation}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Custom CSS for animations */}
      <style jsx>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fadeInLeft {
          from {
            opacity: 0;
            transform: translateX(-20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        @keyframes fadeInRight {
          from {
            opacity: 0;
            transform: translateX(20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        @keyframes float {
          0%, 100% {
            transform: translateY(0px) rotate(0deg);
          }
          25% {
            transform: translateY(-10px) rotate(2deg);
          }
          50% {
            transform: translateY(-20px) rotate(0deg);
          }
          75% {
            transform: translateY(-10px) rotate(-2deg);
          }
        }

        .animate-fadeInUp {
          animation: fadeInUp 0.8s ease-out forwards;
        }

        .animate-fadeInLeft {
          animation: fadeInLeft 0.8s ease-out forwards;
        }

        .animate-fadeInRight {
          animation: fadeInRight 0.8s ease-out forwards;
        }

        .animate-float {
          animation: float linear infinite;
        }
      `}</style>
    </div>
  );
};

export default SmartTaskPlanner;