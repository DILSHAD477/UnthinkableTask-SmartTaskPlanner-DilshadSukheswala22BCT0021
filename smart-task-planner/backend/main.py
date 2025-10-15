from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, timezone
import json
import uuid
from enum import Enum
import asyncio
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lifespan events for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 SmartPlan AI Backend Starting Up...")
    logger.info("✅ AI Task Generation Engine: Ready")
    logger.info("✅ Risk Assessment Module: Loaded")
    logger.info("✅ Timeline Optimization: Active")
    yield
    # Shutdown
    logger.info("🔄 SmartPlan AI Backend Shutting Down...")

app = FastAPI(
    title="SmartPlan AI - Intelligent Task Planning API",
    description="AI-powered task planning with intelligent breakdown, risk assessment, and timeline optimization",
    version="2.0.0",
    lifespan=lifespan
)

# Enhanced CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "https://*.vercel.app",
        "https://*.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"

class GoalInput(BaseModel):
    goal: str = Field(..., description="The main goal to break down", min_length=3)
    deadline: Optional[datetime] = Field(None, description="Target completion date")
    context: Optional[str] = Field(None, description="Additional context or constraints")
    domain: Optional[str] = Field("general", description="Domain type")
    resources: Optional[List[str]] = Field([], description="Available resources")
    working_hours_per_day: Optional[int] = Field(8, description="Working hours per day", ge=1, le=24)
    user_id: Optional[str] = Field(None, description="User identifier for tracking")
    priority_level: Optional[str] = Field("medium", description="Overall project priority")

class TaskOutput(BaseModel):
    id: str
    title: str
    description: str
    priority: TaskPriority
    estimated_hours: float
    dependencies: List[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    risk_factors: List[str]
    success_criteria: List[str]
    resources_needed: List[str]
    status: TaskStatus = TaskStatus.PENDING
    completion_percentage: float = Field(0.0, ge=0.0, le=100.0)
    estimated_cost: Optional[float] = Field(None, description="Estimated cost in USD")

class MilestoneOutput(BaseModel):
    id: str
    percentage: int
    title: str
    date: datetime
    key_task: str
    description: str
    deliverables: List[str] = []
    stakeholders: List[str] = []

class RiskAssessment(BaseModel):
    timeline_risk: str
    resource_risk: str
    complexity_risk: str
    budget_risk: str = "medium"
    technical_risk: str = "medium"
    stakeholder_risk: str = "low"
    high_risk_tasks: int
    critical_path_risks: int
    total_estimated_hours: float
    risk_mitigation_strategies: List[str] = []

class PlanOutput(BaseModel):
    plan_id: str
    goal: str
    total_estimated_hours: float
    critical_path_duration: int
    confidence_score: float
    tasks: List[TaskOutput]
    dependencies_graph: Dict[str, List[str]]
    milestones: List[MilestoneOutput]
    risk_assessment: RiskAssessment
    recommendations: List[str]
    estimated_budget: Optional[float] = None
    success_probability: float = 0.8
    created_at: datetime
    updated_at: datetime

def get_utc_now():
    """Get timezone-aware UTC datetime"""
    return datetime.now(timezone.utc)

def ensure_timezone_aware(dt):
    """Ensure datetime is timezone-aware"""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

class SmartTaskPlannerEngine:
    def __init__(self):
        self.domain_templates = self._load_domain_templates()
        self.risk_patterns = self._load_risk_patterns()
        self.cost_estimates = self._load_cost_estimates()
        
    def _load_domain_templates(self) -> Dict[str, Any]:
        """Enhanced domain-specific templates"""
        return {
            "business": {
                "phases": ["market_analysis", "planning", "execution", "monitoring", "optimization"],
                "typical_tasks": {
                    "market_analysis": [
                        "competitive_analysis", "target_audience_research", "market_sizing",
                        "trend_analysis", "swot_analysis"
                    ],
                    "planning": [
                        "business_plan_creation", "financial_modeling", "resource_allocation",
                        "timeline_development", "risk_assessment"
                    ],
                    "execution": [
                        "team_assembly", "process_implementation", "quality_control",
                        "progress_monitoring", "stakeholder_communication"
                    ]
                }
            },
            "technical": {
                "phases": ["requirements", "design", "development", "testing", "deployment"],
                "typical_tasks": {
                    "requirements": [
                        "requirements_gathering", "technical_specification", "architecture_design"
                    ],
                    "design": [
                        "system_design", "ui_ux_design", "database_design"
                    ],
                    "development": [
                        "core_development", "integration", "code_review"
                    ],
                    "testing": [
                        "unit_testing", "integration_testing", "user_acceptance_testing"
                    ],
                    "deployment": [
                        "environment_setup", "deployment_automation", "monitoring_setup"
                    ]
                }
            },
            "personal": {
                "phases": ["goal_setting", "planning", "skill_development", "implementation"],
                "typical_tasks": {
                    "goal_setting": ["vision_clarification", "smart_goals_definition"],
                    "planning": ["action_plan_creation", "resource_identification"],
                    "skill_development": ["skill_assessment", "learning_path_design"],
                    "implementation": ["daily_actions", "progress_tracking"]
                }
            }
        }
    
    def _load_risk_patterns(self) -> Dict[str, List[str]]:
        """Risk patterns based on historical project data"""
        return {
            "timeline_risks": [
                "Underestimated task complexity",
                "Resource availability conflicts",
                "External dependency delays",
                "Scope creep during execution"
            ],
            "resource_risks": [
                "Key team member unavailability",
                "Budget constraints",
                "Skill gaps in team",
                "Tool/technology limitations"
            ],
            "technical_risks": [
                "Technology compatibility issues",
                "Performance bottlenecks",
                "Security vulnerabilities",
                "Integration complexities"
            ]
        }
    
    def _load_cost_estimates(self) -> Dict[str, Dict[str, float]]:
        """Cost estimation patterns by domain"""
        return {
            "business": {
                "market_research": 2500,
                "planning": 1500,
                "execution": 10000,
                "monitoring": 2000
            },
            "technical": {
                "requirements": 3000,
                "design": 5000,
                "development": 15000,
                "testing": 4000,
                "deployment": 2000
            },
            "personal": {
                "goal_setting": 0,
                "planning": 100,
                "skill_development": 1000,
                "implementation": 500
            }
        }

    async def generate_enhanced_plan(self, goal_input: GoalInput) -> PlanOutput:
        """Generate comprehensive task plan with enhanced AI intelligence"""
        
        logger.info(f"🎯 Generating plan for goal: {goal_input.goal[:50]}...")
        
        # Analyze goal complexity
        complexity_score = self._analyze_goal_complexity(goal_input.goal)
        
        # Generate tasks based on sophisticated patterns
        tasks_data = await self._generate_intelligent_tasks(goal_input, complexity_score)
        
        # Create task objects with enhanced properties
        tasks = self._create_enhanced_tasks(tasks_data, goal_input)
        
        # Advanced timeline optimization
        optimized_timeline = self._optimize_timeline_advanced(tasks, goal_input)
        
        # Comprehensive risk assessment
        risk_assessment = self._comprehensive_risk_assessment(optimized_timeline, goal_input, complexity_score)
        
        # Generate intelligent recommendations
        recommendations = self._generate_intelligent_recommendations(optimized_timeline, risk_assessment, goal_input)
        
        # Create enhanced milestones
        milestones = self._create_enhanced_milestones(optimized_timeline)
        
        # Calculate success probability
        success_probability = self._calculate_success_probability(optimized_timeline, risk_assessment)
        
        # Estimate budget
        estimated_budget = self._estimate_project_budget(optimized_timeline, goal_input.domain)
        
        current_time = get_utc_now()
        
        plan_output = PlanOutput(
            plan_id=f"plan_{uuid.uuid4().hex[:8]}",
            goal=goal_input.goal,
            total_estimated_hours=sum(task.estimated_hours for task in optimized_timeline),
            critical_path_duration=self._calculate_critical_path_duration(optimized_timeline),
            confidence_score=self._calculate_overall_confidence(optimized_timeline),
            tasks=optimized_timeline,
            dependencies_graph=self._create_dependencies_graph(optimized_timeline),
            milestones=milestones,
            risk_assessment=risk_assessment,
            recommendations=recommendations,
            estimated_budget=estimated_budget,
            success_probability=success_probability,
            created_at=current_time,
            updated_at=current_time
        )
        
        logger.info(f"✅ Plan generated successfully: {len(tasks)} tasks, {plan_output.critical_path_duration} days duration")
        return plan_output

    def _analyze_goal_complexity(self, goal: str) -> float:
        """Analyze goal complexity using various factors"""
        complexity_factors = {
            'length': min(len(goal.split()) / 50, 1.0),
            'keywords': self._count_complexity_keywords(goal) / 20,
            'specificity': self._measure_specificity(goal)
        }
        return sum(complexity_factors.values()) / len(complexity_factors)

    def _count_complexity_keywords(self, goal: str) -> int:
        """Count keywords that indicate complexity"""
        complex_keywords = [
            'integrate', 'develop', 'implement', 'optimize', 'analyze', 'design',
            'research', 'coordinate', 'manage', 'launch', 'scale', 'automate'
        ]
        return sum(1 for keyword in complex_keywords if keyword in goal.lower())

    def _measure_specificity(self, goal: str) -> float:
        """Measure how specific the goal is"""
        specific_indicators = ['by', 'within', 'using', 'for', 'with', 'through']
        specificity_score = sum(1 for indicator in specific_indicators if indicator in goal.lower())
        return min(specificity_score / 3, 1.0)

    async def _generate_intelligent_tasks(self, goal_input: GoalInput, complexity_score: float) -> List[Dict]:
        """Generate tasks with enhanced intelligence"""
        
        goal_lower = goal_input.goal.lower()
        
        # Determine task generation strategy based on goal keywords
        if any(word in goal_lower for word in ["launch", "product", "app", "website", "platform"]):
            return self._generate_product_launch_tasks(goal_input, complexity_score)
        elif any(word in goal_lower for word in ["learn", "study", "master", "skill", "training"]):
            return self._generate_learning_tasks(goal_input, complexity_score)
        elif any(word in goal_lower for word in ["research", "analyze", "investigate", "study"]):
            return self._generate_research_tasks(goal_input, complexity_score)
        elif any(word in goal_lower for word in ["organize", "event", "conference", "meeting"]):
            return self._generate_event_tasks(goal_input, complexity_score)
        else:
            return self._generate_generic_tasks(goal_input, complexity_score)

    def _generate_product_launch_tasks(self, goal_input: GoalInput, complexity_score: float) -> List[Dict]:
        """Generate product launch tasks"""
        base_hours = 200 * (1 + complexity_score)
        
        return [
            {
                "title": "Market Research & Competitive Analysis",
                "description": "Comprehensive market analysis, competitor research, and target audience identification",
                "priority": "high",
                "estimated_hours": base_hours * 0.15,
                "dependencies": [],
                "risk_factors": [
                    "Market assumptions may be incorrect",
                    "Limited access to competitor data",
                    "Target audience may be broader than expected"
                ],
                "success_criteria": [
                    "Market size quantified and documented",
                    "Top 5 competitors analyzed thoroughly",
                    "Target audience personas created"
                ],
                "resources_needed": ["Market research tools", "Survey platform", "Analytics team"]
            },
            {
                "title": "Product Strategy & Roadmap Development",
                "description": "Define product vision, strategy, feature roadmap, and success metrics",
                "priority": "critical",
                "estimated_hours": base_hours * 0.10,
                "dependencies": ["Market Research & Competitive Analysis"],
                "risk_factors": [
                    "Stakeholder alignment challenges",
                    "Feature prioritization conflicts",
                    "Timeline constraints"
                ],
                "success_criteria": [
                    "Product strategy document approved",
                    "Feature roadmap prioritized",
                    "Success metrics defined"
                ],
                "resources_needed": ["Product manager", "Strategy team", "Stakeholders"]
            },
            {
                "title": "MVP Development & Implementation",
                "description": "Build minimum viable product with core features and essential functionality",
                "priority": "critical",
                "estimated_hours": base_hours * 0.40,
                "dependencies": ["Product Strategy & Roadmap Development"],
                "risk_factors": [
                    "Technical complexity underestimated",
                    "Resource availability issues",
                    "Integration challenges"
                ],
                "success_criteria": [
                    "Core features fully functional",
                    "Code quality standards met",
                    "Basic security measures implemented"
                ],
                "resources_needed": ["Development team", "UI/UX designer", "Development tools"]
            },
            {
                "title": "Quality Assurance & Testing",
                "description": "Comprehensive testing including unit, integration, and user acceptance testing",
                "priority": "high",
                "estimated_hours": base_hours * 0.15,
                "dependencies": ["MVP Development & Implementation"],
                "risk_factors": [
                    "Critical bugs discovered late",
                    "Performance issues under load",
                    "User acceptance criteria not met"
                ],
                "success_criteria": [
                    "All critical bugs resolved",
                    "Performance benchmarks achieved",
                    "User acceptance testing passed"
                ],
                "resources_needed": ["QA engineer", "Testing tools", "Test users"]
            },
            {
                "title": "Marketing Campaign & Launch Preparation",
                "description": "Develop and execute marketing strategy, create launch materials, and build awareness",
                "priority": "medium",
                "estimated_hours": base_hours * 0.12,
                "dependencies": ["Product Strategy & Roadmap Development"],
                "risk_factors": [
                    "Marketing message not resonating",
                    "Launch timing conflicts",
                    "Budget constraints"
                ],
                "success_criteria": [
                    "Marketing campaign materials ready",
                    "Launch timeline finalized",
                    "PR and media outreach completed"
                ],
                "resources_needed": ["Marketing team", "Content creator", "Design tools"]
            },
            {
                "title": "Production Deployment & Go-Live",
                "description": "Deploy to production, monitor system performance, and execute official launch",
                "priority": "critical",
                "estimated_hours": base_hours * 0.08,
                "dependencies": ["Quality Assurance & Testing", "Marketing Campaign & Launch Preparation"],
                "risk_factors": [
                    "Deployment failures",
                    "System performance issues",
                    "User adoption slower than expected"
                ],
                "success_criteria": [
                    "Successful production deployment",
                    "Monitoring systems active",
                    "Launch executed successfully"
                ],
                "resources_needed": ["DevOps team", "Monitoring tools", "Support team"]
            }
        ]

    def _generate_learning_tasks(self, goal_input: GoalInput, complexity_score: float) -> List[Dict]:
        """Generate learning path tasks"""
        base_hours = 120 * (1 + complexity_score)
        
        return [
            {
                "title": "Learning Path Research & Planning",
                "description": "Research best learning resources, create study plan, and set up learning environment",
                "priority": "high",
                "estimated_hours": base_hours * 0.10,
                "dependencies": [],
                "risk_factors": [
                    "Information overload from too many resources",
                    "Poor quality learning materials selected"
                ],
                "success_criteria": [
                    "3-5 high-quality resources identified",
                    "Structured learning schedule created",
                    "Learning environment set up"
                ],
                "resources_needed": ["Learning platforms", "Study materials", "Note-taking tools"]
            },
            {
                "title": "Foundation Knowledge Building",
                "description": "Study fundamental concepts and build strong theoretical foundation",
                "priority": "critical",
                "estimated_hours": base_hours * 0.40,
                "dependencies": ["Learning Path Research & Planning"],
                "risk_factors": [
                    "Concepts too difficult to understand",
                    "Lack of motivation over time",
                    "Insufficient practice time"
                ],
                "success_criteria": [
                    "Core concepts mastered",
                    "Knowledge gaps identified and addressed",
                    "Self-assessment tests passed"
                ],
                "resources_needed": ["Study materials", "Practice environment", "Mentor support"]
            },
            {
                "title": "Hands-on Practice & Application",
                "description": "Apply learned concepts through practical exercises and real-world projects",
                "priority": "high",
                "estimated_hours": base_hours * 0.35,
                "dependencies": ["Foundation Knowledge Building"],
                "risk_factors": [
                    "Difficulty applying theoretical knowledge",
                    "Technical setup challenges",
                    "Project scope too ambitious"
                ],
                "success_criteria": [
                    "5+ practice exercises completed successfully",
                    "Portfolio project built and documented",
                    "Skills demonstrated through practical work"
                ],
                "resources_needed": ["Development environment", "Project tools", "Practice datasets"]
            },
            {
                "title": "Knowledge Validation & Assessment",
                "description": "Test understanding through assessments, peer review, and certification",
                "priority": "medium",
                "estimated_hours": base_hours * 0.15,
                "dependencies": ["Hands-on Practice & Application"],
                "risk_factors": [
                    "Assessment reveals knowledge gaps",
                    "Certification requirements not met"
                ],
                "success_criteria": [
                    "Assessment passed with good score",
                    "Peer feedback positive",
                    "Certification obtained (if applicable)"
                ],
                "resources_needed": ["Assessment platform", "Study group", "Certification body"]
            }
        ]

    def _generate_research_tasks(self, goal_input: GoalInput, complexity_score: float) -> List[Dict]:
        """Generate research project tasks"""
        base_hours = 150 * (1 + complexity_score)
        
        return [
            {
                "title": "Research Question & Methodology Design",
                "description": "Define research questions, develop methodology, and plan research approach",
                "priority": "critical",
                "estimated_hours": base_hours * 0.20,
                "dependencies": [],
                "risk_factors": [
                    "Research questions too broad or narrow",
                    "Methodology not suitable for questions"
                ],
                "success_criteria": [
                    "Clear research questions formulated",
                    "Methodology approved by stakeholders",
                    "Research plan documented"
                ],
                "resources_needed": ["Research tools", "Academic databases", "Expert consultation"]
            },
            {
                "title": "Literature Review & Background Research",
                "description": "Comprehensive review of existing literature and background research",
                "priority": "high",
                "estimated_hours": base_hours * 0.30,
                "dependencies": ["Research Question & Methodology Design"],
                "risk_factors": [
                    "Insufficient relevant literature available",
                    "Information sources outdated"
                ],
                "success_criteria": [
                    "Comprehensive literature review completed",
                    "Research gaps identified",
                    "Background knowledge established"
                ],
                "resources_needed": ["Academic databases", "Library access", "Reference management tools"]
            },
            {
                "title": "Data Collection & Analysis",
                "description": "Collect data according to methodology and perform comprehensive analysis",
                "priority": "critical",
                "estimated_hours": base_hours * 0.35,
                "dependencies": ["Literature Review & Background Research"],
                "risk_factors": [
                    "Data collection challenges",
                    "Sample size insufficient",
                    "Analysis tools inadequate"
                ],
                "success_criteria": [
                    "Required data collected successfully",
                    "Analysis completed using appropriate methods",
                    "Results documented and validated"
                ],
                "resources_needed": ["Data collection tools", "Analysis software", "Statistical expertise"]
            },
            {
                "title": "Report Writing & Documentation",
                "description": "Compile findings into comprehensive research report with conclusions",
                "priority": "high",
                "estimated_hours": base_hours * 0.15,
                "dependencies": ["Data Collection & Analysis"],
                "risk_factors": [
                    "Findings difficult to interpret",
                    "Writing and presentation challenges"
                ],
                "success_criteria": [
                    "Research report completed",
                    "Findings clearly presented",
                    "Conclusions supported by data"
                ],
                "resources_needed": ["Writing tools", "Data visualization software", "Peer reviewers"]
            }
        ]

    def _generate_event_tasks(self, goal_input: GoalInput, complexity_score: float) -> List[Dict]:
        """Generate event organization tasks"""
        base_hours = 100 * (1 + complexity_score)
        
        return [
            {
                "title": "Event Planning & Strategy Development",
                "description": "Define event objectives, format, audience, and overall strategy",
                "priority": "critical",
                "estimated_hours": base_hours * 0.20,
                "dependencies": [],
                "risk_factors": [
                    "Unclear event objectives",
                    "Target audience not well defined"
                ],
                "success_criteria": [
                    "Event strategy documented",
                    "Target audience identified",
                    "Success metrics defined"
                ],
                "resources_needed": ["Planning tools", "Market research", "Stakeholder input"]
            },
            {
                "title": "Venue & Logistics Coordination",
                "description": "Secure venue, coordinate catering, equipment, and logistical requirements",
                "priority": "high",
                "estimated_hours": base_hours * 0.30,
                "dependencies": ["Event Planning & Strategy Development"],
                "risk_factors": [
                    "Venue availability issues",
                    "Logistics coordination challenges",
                    "Budget constraints"
                ],
                "success_criteria": [
                    "Venue booked and confirmed",
                    "Catering arrangements finalized",
                    "Equipment and AV needs secured"
                ],
                "resources_needed": ["Venue contacts", "Catering services", "AV equipment"]
            },
            {
                "title": "Content & Speaker Management",
                "description": "Recruit speakers, develop content agenda, and coordinate presentations",
                "priority": "high",
                "estimated_hours": base_hours * 0.25,
                "dependencies": ["Event Planning & Strategy Development"],
                "risk_factors": [
                    "Speaker cancellations",
                    "Content quality concerns",
                    "Schedule conflicts"
                ],
                "success_criteria": [
                    "Speaker lineup confirmed",
                    "Content agenda finalized",
                    "Presentation materials ready"
                ],
                "resources_needed": ["Speaker network", "Content management tools", "Presentation software"]
            },
            {
                "title": "Marketing & Registration Management",
                "description": "Promote event, manage registrations, and handle attendee communications",
                "priority": "medium",
                "estimated_hours": base_hours * 0.15,
                "dependencies": ["Venue & Logistics Coordination"],
                "risk_factors": [
                    "Low registration numbers",
                    "Marketing reach insufficient"
                ],
                "success_criteria": [
                    "Registration target achieved",
                    "Marketing campaign executed",
                    "Attendee communications managed"
                ],
                "resources_needed": ["Registration platform", "Marketing channels", "Email system"]
            },
            {
                "title": "Event Execution & Follow-up",
                "description": "Execute event operations and conduct post-event follow-up activities",
                "priority": "critical",
                "estimated_hours": base_hours * 0.10,
                "dependencies": ["Content & Speaker Management", "Marketing & Registration Management"],
                "risk_factors": [
                    "Day-of-event operational issues",
                    "Technology failures"
                ],
                "success_criteria": [
                    "Event executed smoothly",
                    "Attendee satisfaction high",
                    "Follow-up activities completed"
                ],
                "resources_needed": ["Event staff", "Technical support", "Feedback tools"]
            }
        ]

    def _generate_generic_tasks(self, goal_input: GoalInput, complexity_score: float) -> List[Dict]:
        """Generate generic tasks for any goal"""
        base_hours = 80 * (1 + complexity_score)
        
        return [
            {
                "title": "Goal Analysis & Planning",
                "description": "Break down the goal into specific components and create detailed action plan",
                "priority": "high",
                "estimated_hours": base_hours * 0.20,
                "dependencies": [],
                "risk_factors": [
                    "Goal not clearly defined",
                    "Missing key requirements",
                    "Unrealistic expectations"
                ],
                "success_criteria": [
                    "Goal clearly defined and documented",
                    "Action plan created with milestones",
                    "Success metrics identified"
                ],
                "resources_needed": ["Planning tools", "Research resources", "Stakeholder input"]
            },
            {
                "title": "Resource Gathering & Preparation",
                "description": "Identify and secure necessary resources, tools, and support systems",
                "priority": "medium",
                "estimated_hours": base_hours * 0.25,
                "dependencies": ["Goal Analysis & Planning"],
                "risk_factors": [
                    "Resources not available when needed",
                    "Budget constraints",
                    "Access limitations"
                ],
                "success_criteria": [
                    "All required resources identified",
                    "Tools and materials acquired",
                    "Support systems established"
                ],
                "resources_needed": ["Budget allocation", "Vendor contacts", "Team members"]
            },
            {
                "title": "Core Implementation & Execution",
                "description": "Execute the main activities required to achieve the goal",
                "priority": "critical",
                "estimated_hours": base_hours * 0.40,
                "dependencies": ["Resource Gathering & Preparation"],
                "risk_factors": [
                    "Implementation challenges",
                    "Unexpected obstacles",
                    "Timeline pressures"
                ],
                "success_criteria": [
                    "Key deliverables completed",
                    "Quality standards maintained",
                    "Progress milestones achieved"
                ],
                "resources_needed": ["Project team", "Tools and equipment", "Work environment"]
            },
            {
                "title": "Review, Optimization & Completion",
                "description": "Review work quality, optimize outcomes, and finalize deliverables",
                "priority": "high",
                "estimated_hours": base_hours * 0.15,
                "dependencies": ["Core Implementation & Execution"],
                "risk_factors": [
                    "Quality issues discovered",
                    "Optimization time insufficient",
                    "Final approval delays"
                ],
                "success_criteria": [
                    "Quality review completed successfully",
                    "Optimizations implemented",
                    "Final deliverables approved"
                ],
                "resources_needed": ["Review team", "Quality tools", "Approval stakeholders"]
            }
        ]

    def _create_enhanced_tasks(self, tasks_data: List[Dict], goal_input: GoalInput) -> List[TaskOutput]:
        """Create enhanced TaskOutput objects"""
        enhanced_tasks = []
        
        for i, task_data in enumerate(tasks_data):
            task = TaskOutput(
                id=f"task_{uuid.uuid4().hex[:8]}",
                title=task_data["title"],
                description=task_data["description"],
                priority=TaskPriority(task_data["priority"]),
                estimated_hours=float(task_data["estimated_hours"]),
                dependencies=task_data.get("dependencies", []),
                start_date=None,  # Will be calculated in timeline optimization
                end_date=None,
                confidence_score=self._calculate_task_confidence(task_data),
                risk_factors=task_data.get("risk_factors", []),
                success_criteria=task_data.get("success_criteria", []),
                resources_needed=task_data.get("resources_needed", []),
                status=TaskStatus.PENDING,
                completion_percentage=0.0,
                estimated_cost=self._estimate_task_cost(task_data, goal_input.domain)
            )
            enhanced_tasks.append(task)
        
        return enhanced_tasks

    def _calculate_task_confidence(self, task_data: Dict) -> float:
        """Calculate confidence score for task completion"""
        base_confidence = 0.85
        
        # Reduce confidence based on number of risk factors
        risk_penalty = len(task_data.get("risk_factors", [])) * 0.05
        
        # Reduce confidence for very large tasks
        if task_data["estimated_hours"] > 50:
            risk_penalty += 0.1
        
        # Increase confidence if success criteria are well defined
        if len(task_data.get("success_criteria", [])) >= 3:
            base_confidence += 0.05
        
        return max(0.4, min(1.0, base_confidence - risk_penalty))

    def _estimate_task_cost(self, task_data: Dict, domain: str) -> Optional[float]:
        """Estimate task cost based on domain"""
        hourly_rates = {
            "technical": 100,
            "business": 75,
            "academic": 50,
            "personal": 25,
            "creative": 60
        }
        rate = hourly_rates.get(domain, 75)
        return task_data["estimated_hours"] * rate

    def _optimize_timeline_advanced(self, tasks: List[TaskOutput], goal_input: GoalInput) -> List[TaskOutput]:
        """Advanced timeline optimization with dependency management"""
        
        # Create task mapping
        task_map = {task.title: task for task in tasks}
        
        # Calculate start and end dates considering dependencies
        current_date = ensure_timezone_aware(get_utc_now())
        
        def calculate_task_schedule(task: TaskOutput, scheduled_tasks: Dict[str, TaskOutput]) -> None:
            if task.start_date:  # Already scheduled
                return
            
            # Find latest end date of dependencies
            latest_dependency_end = current_date
            for dep_title in task.dependencies:
                if dep_title in task_map:
                    dep_task = task_map[dep_title]
                    if dep_task.title not in scheduled_tasks:
                        calculate_task_schedule(dep_task, scheduled_tasks)
                    if dep_task.end_date and dep_task.end_date > latest_dependency_end:
                        latest_dependency_end = dep_task.end_date
            
            # Calculate task duration in days
            hours_per_day = goal_input.working_hours_per_day
            duration_days = max(1, task.estimated_hours / hours_per_day)
            
            # Set start and end dates (timezone-aware)
            task.start_date = latest_dependency_end
            task.end_date = task.start_date + timedelta(days=duration_days)
            
            scheduled_tasks[task.title] = task
        
        # Schedule all tasks
        scheduled_tasks = {}
        for task in tasks:
            calculate_task_schedule(task, scheduled_tasks)
        
        return tasks

    def _comprehensive_risk_assessment(self, tasks: List[TaskOutput], goal_input: GoalInput, complexity_score: float) -> RiskAssessment:
        """Comprehensive risk assessment"""
        
        total_hours = sum(task.estimated_hours for task in tasks)
        high_risk_tasks = len([t for t in tasks if len(t.risk_factors) > 2])
        critical_tasks = len([t for t in tasks if t.priority == TaskPriority.CRITICAL])
        
        # Timeline risk assessment
        if goal_input.deadline:
            deadline = ensure_timezone_aware(goal_input.deadline)
            current_time = get_utc_now()
            days_available = (deadline - current_time).days
            required_daily_hours = total_hours / max(days_available, 1)
            available_daily_hours = goal_input.working_hours_per_day
            
            if required_daily_hours > available_daily_hours * 1.3:
                timeline_risk = "high"
            elif required_daily_hours > available_daily_hours * 1.1:
                timeline_risk = "medium"
            else:
                timeline_risk = "low"
        else:
            timeline_risk = "medium"
        
        # Resource risk assessment
        if not goal_input.resources:
            resource_risk = "high"
        elif len(goal_input.resources) < 3:
            resource_risk = "medium"
        else:
            resource_risk = "low"
        
        # Complexity risk
        if complexity_score > 0.8:
            complexity_risk = "high"
        elif complexity_score > 0.5:
            complexity_risk = "medium"
        else:
            complexity_risk = "low"
        
        # Risk mitigation strategies
        mitigation_strategies = []
        if timeline_risk == "high":
            mitigation_strategies.append("Consider scope reduction or deadline extension")
        if resource_risk == "high":
            mitigation_strategies.append("Identify and allocate dedicated team members")
        if complexity_risk == "high":
            mitigation_strategies.append("Break down complex tasks into smaller components")
        
        return RiskAssessment(
            timeline_risk=timeline_risk,
            resource_risk=resource_risk,
            complexity_risk=complexity_risk,
            high_risk_tasks=high_risk_tasks,
            critical_path_risks=critical_tasks,
            total_estimated_hours=total_hours,
            risk_mitigation_strategies=mitigation_strategies
        )

    def _generate_intelligent_recommendations(self, tasks: List[TaskOutput], risk_assessment: RiskAssessment, goal_input: GoalInput) -> List[str]:
        """Generate intelligent recommendations"""
        
        recommendations = []
        
        # Timeline-based recommendations
        if risk_assessment.timeline_risk == "high":
            recommendations.append("🚨 Consider extending deadline by 20-30% or reducing scope to ensure quality delivery")
            recommendations.append("⚡ Implement parallel task execution where dependencies allow")
        
        # Resource-based recommendations
        if risk_assessment.resource_risk == "high":
            recommendations.append("👥 Allocate dedicated team members and define clear roles and responsibilities")
            recommendations.append("🔧 Invest in proper tools and infrastructure to maximize team productivity")
        
        # Risk mitigation recommendations
        if risk_assessment.high_risk_tasks > 3:
            recommendations.append("🛡️ Develop contingency plans for high-risk tasks and identify early warning indicators")
            recommendations.append("🔄 Implement weekly risk review sessions to proactively address emerging issues")
        
        # Quality assurance recommendations
        if len(tasks) > 8:
            recommendations.append("✅ Establish quality gates and milestone reviews to ensure deliverable standards")
            recommendations.append("📊 Set up progress tracking dashboard with real-time visibility for stakeholders")
        
        # Default recommendations
        recommendations.append("🎯 Define clear success metrics and KPIs to measure progress objectively")
        recommendations.append("💬 Schedule regular stakeholder check-ins to ensure alignment and gather feedback")
        
        return recommendations

    def _create_enhanced_milestones(self, tasks: List[TaskOutput]) -> List[MilestoneOutput]:
        """Create enhanced milestones"""
        milestones = []
        total_hours = sum(task.estimated_hours for task in tasks)
        cumulative_hours = 0
        milestone_percentages = [25, 50, 75, 100]
        
        sorted_tasks = sorted([t for t in tasks if t.end_date], key=lambda x: x.end_date)
        
        for task in sorted_tasks:
            cumulative_hours += task.estimated_hours
            completion_percentage = (cumulative_hours / total_hours) * 100
            
            for milestone_pct in milestone_percentages[:]:
                if completion_percentage >= milestone_pct:
                    milestone = MilestoneOutput(
                        id=f"milestone_{uuid.uuid4().hex[:6]}",
                        percentage=milestone_pct,
                        title=f"Project {milestone_pct}% Complete",
                        date=task.end_date,
                        key_task=task.title,
                        description=f"Milestone achieved with completion of '{task.title}' - {milestone_pct}% of total project scope delivered",
                        deliverables=[
                            f"All tasks up to '{task.title}' completed",
                            f"{milestone_pct}% of project scope delivered"
                        ],
                        stakeholders=["Project Manager", "Team Lead", "Stakeholders"]
                    )
                    milestones.append(milestone)
                    milestone_percentages.remove(milestone_pct)
        
        return milestones

    def _calculate_success_probability(self, tasks: List[TaskOutput], risk_assessment: RiskAssessment) -> float:
        """Calculate overall project success probability"""
        
        # Base probability
        base_probability = 0.8
        
        # Confidence factor
        avg_confidence = sum(task.confidence_score for task in tasks) / len(tasks) if tasks else 0.5
        confidence_factor = avg_confidence
        
        # Risk factor
        risk_scores = {
            "low": 0.9,
            "medium": 0.7,
            "high": 0.4
        }
        
        risk_factor = (
            risk_scores.get(risk_assessment.timeline_risk, 0.7) * 0.4 +
            risk_scores.get(risk_assessment.resource_risk, 0.7) * 0.3 +
            risk_scores.get(risk_assessment.complexity_risk, 0.7) * 0.3
        )
        
        # Calculate final probability
        success_probability = base_probability * confidence_factor * risk_factor
        return max(0.2, min(0.95, success_probability))

    def _estimate_project_budget(self, tasks: List[TaskOutput], domain: str) -> Optional[float]:
        """Estimate total project budget"""
        total_budget = 0
        
        for task in tasks:
            if task.estimated_cost:
                total_budget += task.estimated_cost
        
        return total_budget if total_budget > 0 else None

    def _calculate_critical_path_duration(self, tasks: List[TaskOutput]) -> int:
        """Calculate critical path duration"""
        if not tasks or not any(task.end_date for task in tasks):
            return 0
        
        start_date = min(task.start_date for task in tasks if task.start_date)
        end_date = max(task.end_date for task in tasks if task.end_date)
        
        return (end_date - start_date).days + 1

    def _calculate_overall_confidence(self, tasks: List[TaskOutput]) -> float:
        """Calculate weighted overall confidence score"""
        if not tasks:
            return 0.0
        
        total_weighted_confidence = sum(task.confidence_score * task.estimated_hours for task in tasks)
        total_hours = sum(task.estimated_hours for task in tasks)
        
        return total_weighted_confidence / total_hours if total_hours > 0 else 0.0

    def _create_dependencies_graph(self, tasks: List[TaskOutput]) -> Dict[str, List[str]]:
        """Create dependencies graph"""
        graph = {}
        task_title_to_id = {task.title: task.id for task in tasks}
        
        for task in tasks:
            dependencies = []
            for dep_title in task.dependencies:
                if dep_title in task_title_to_id:
                    dependencies.append(task_title_to_id[dep_title])
            graph[task.id] = dependencies
        
        return graph

# Initialize the enhanced planning engine
planner = SmartTaskPlannerEngine()

# Enhanced API endpoints
@app.post("/api/create-plan", response_model=PlanOutput)
async def create_enhanced_plan(goal_input: GoalInput, background_tasks: BackgroundTasks):
    """Create an enhanced intelligent task plan"""
    try:
        logger.info(f"📥 Received plan creation request for goal: {goal_input.goal[:50]}...")
        
        # Generate the enhanced plan
        plan = await planner.generate_enhanced_plan(goal_input)
        
        # Add background task for analytics
        background_tasks.add_task(log_plan_creation, plan.plan_id, goal_input.goal)
        
        logger.info(f"✅ Plan created successfully: {plan.plan_id}")
        return plan
        
    except Exception as e:
        logger.error(f"❌ Error creating plan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Plan creation failed: {str(e)}")

@app.get("/api/health")
async def enhanced_health_check():
    """Enhanced health check"""
    return {
        "status": "healthy",
        "timestamp": get_utc_now(),
        "version": "2.0.0",
        "services": {
            "ai_engine": "operational",
            "risk_assessment": "operational",
            "timeline_optimizer": "operational"
        },
        "uptime": "System running normally"
    }

@app.get("/api/domains")
async def get_available_domains():
    """Get available domains with descriptions"""
    domains = {
        "business": {
            "name": "Business",
            "description": "Business projects, product launches, market analysis",
            "typical_duration": "2-6 months",
            "complexity": "medium-high"
        },
        "technical": {
            "name": "Technical",
            "description": "Software development, system implementation, technical projects",
            "typical_duration": "1-4 months",
            "complexity": "high"
        },
        "personal": {
            "name": "Personal",
            "description": "Personal goals, skill development, lifestyle changes",
            "typical_duration": "1-3 months",
            "complexity": "low-medium"
        },
        "academic": {
            "name": "Academic",
            "description": "Research projects, academic studies, educational goals",
            "typical_duration": "3-12 months",
            "complexity": "medium"
        },
        "creative": {
            "name": "Creative",
            "description": "Creative projects, artistic endeavors, content creation",
            "typical_duration": "2-8 weeks",
            "complexity": "medium"
        }
    }
    return domains

@app.get("/api/templates")
async def get_project_templates():
    """Get available project templates"""
    return {
        "templates": planner.domain_templates,
        "description": "Domain-specific templates for intelligent task generation"
    }

# Background task functions
async def log_plan_creation(plan_id: str, goal: str):
    """Log plan creation for analytics"""
    logger.info(f"📊 Analytics: Plan {plan_id} created for goal: {goal[:30]}...")

# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": f"Invalid input: {str(exc)}"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again."}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)