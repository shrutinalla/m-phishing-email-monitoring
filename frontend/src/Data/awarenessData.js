export const awarenessStats = [
  {
    title: "Employees Trained",
    value: "182",
    icon: "🎓",
  },
  {
    title: "Completion Rate",
    value: "84%",
    icon: "✅",
  },
  {
    title: "Pending Training",
    value: "34",
    icon: "⏳",
  },
  {
    title: "Average Quiz Score",
    value: "88%",
    icon: "📊",
  },
];

export const awarenessModules = [
  {
    id: 1,
    title: "Recognizing Phishing Emails",
    duration: "15 mins",
    level: "Beginner",
    status: "Completed",
  },
  {
    id: 2,
    title: "Credential Theft Awareness",
    duration: "20 mins",
    level: "Intermediate",
    status: "In Progress",
  },
  {
    id: 3,
    title: "Safe Link Verification",
    duration: "12 mins",
    level: "Beginner",
    status: "Pending",
  },
  {
    id: 4,
    title: "Email Security Best Practices",
    duration: "18 mins",
    level: "Advanced",
    status: "Pending",
  },
];
export const phishingRedFlags = [
  {
    id: 1,
    icon: "📧",
    title: "Fake Sender Address",
    description:
      "Attackers often use email addresses that closely resemble legitimate company domains.",
    example: "security@midhanl.com instead of security@midhani.com",
  },
  {
    id: 2,
    icon: "🔗",
    title: "Suspicious Links",
    description:
      "Hover over links before clicking to verify that the destination matches the official website.",
    example: "https://midhani-login-security.com",
  },
  {
    id: 3,
    icon: "🚨",
    title: "Urgent Language",
    description:
      "Messages creating panic or demanding immediate action are common phishing tactics.",
    example: "\"Your account will be locked in 10 minutes!\"",
  },
  {
    id: 4,
    icon: "📎",
    title: "Unexpected Attachments",
    description:
      "Unexpected attachments may contain malware or malicious macros.",
    example: "Salary_Update.zip",
  },
  {
    id: 5,
    icon: "🔑",
    title: "Credential Requests",
    description:
      "Legitimate organizations rarely ask for passwords through email.",
    example: "\"Verify your password immediately.\"",
  },
  {
    id: 6,
    icon: "✍️",
    title: "Grammar & Spelling Errors",
    description:
      "Many phishing emails contain poor grammar, spelling mistakes, or awkward wording.",
    example: "\"Congratulation! Verify immediately.\"",
  },
];
export const awarenessQuiz = [
  {
    id: 1,
    question: "Which of the following is the strongest indicator of a phishing email?",
    options: [
      "Urgent request for confidential information",
      "Company newsletter",
      "Meeting invitation",
      "Birthday wishes"
    ],
    correctAnswer: 0,
    explanation:
      "Phishing emails often create urgency to pressure victims into revealing sensitive information."
  },

  {
    id: 2,
    question: "What should you do before clicking a link in an email?",
    options: [
      "Click immediately",
      "Reply to the sender first",
      "Hover over the link to verify the URL",
      "Download the attachment"
    ],
    correctAnswer: 2,
    explanation:
      "Always verify the destination URL before clicking any link."
  },

  {
    id: 3,
    question: "Which attachment is most suspicious?",
    options: [
      "Holiday_Photos.zip",
      "Company_Policy.pdf",
      "Meeting_Agenda.docx",
      "Training_Guide.pdf"
    ],
    correctAnswer: 0,
    explanation:
      "Unexpected ZIP files are commonly used to deliver malware."
  },

  {
    id: 4,
    question: "What should you do if you suspect a phishing email?",
    options: [
      "Ignore it",
      "Forward it to the security team",
      "Reply asking if it's real",
      "Open all attachments"
    ],
    correctAnswer: 1,
    explanation:
      "Reporting suspicious emails helps protect the organization."
  },

  {
    id: 5,
    question: "Which email address looks suspicious?",
    options: [
      "security@midhani.in",
      "hr@midhani.in",
      "security@midhanl.in",
      "admin@midhani.in"
    ],
    correctAnswer: 2,
    explanation:
      "Attackers often replace similar-looking characters such as 'i' with 'l'."
  }
];
export const phishingExamples = [
  {
    id: 1,
    difficulty: "Easy",
    sender: "security@midhanl.in",
    subject: "Urgent: Verify Your Account",
    body:
      "Dear Employee,\n\nYour account will be suspended within 24 hours due to unusual activity. Please verify your account immediately by clicking the link below.\n\nhttps://midhani-security-check.com\n\nRegards,\nIT Support",
    warningSigns: [
      "Fake sender domain",
      "Urgent language",
      "Suspicious external link",
      "Requests immediate action"
    ],
    explanation:
      "Attackers often impersonate company security teams and create urgency to trick employees into revealing credentials."
  },

  {
    id: 2,
    difficulty: "Medium",
    sender: "hr@midhani-careers.com",
    subject: "Salary Revision Form",
    body:
      "Dear Employee,\n\nPlease download and complete the attached Salary Revision Form before the end of today.\n\nAttachment: Salary_Revision.zip\n\nRegards,\nHR Department",
    warningSigns: [
      "Look-alike HR domain",
      "Unexpected ZIP attachment",
      "Pressure to act quickly",
      "Unexpected payroll request"
    ],
    explanation:
      "Unexpected ZIP attachments are commonly used to distribute malware disguised as HR documents."
  },

  {
    id: 3,
    difficulty: "Hard",
    sender: "admin@midhani.in",
    subject: "Office 365 Login Required",
    body:
      "Dear User,\n\nWe detected unusual login activity. Please sign in again using the secure portal below.\n\nhttps://login-midhani.secureverify.net\n\nThank you.",
    warningSigns: [
      "Fake login portal",
      "Suspicious URL",
      "Credential harvesting attempt",
      "Generic greeting"
    ],
    explanation:
      "Some phishing emails spoof legitimate email addresses while directing users to fake login pages."
  }
];
export const decisionScenarios = [
  {
    id: 1,
    sender: "security@midhanl.in",
    subject: "Urgent Password Reset",
    body:
      "Your password expires today. Click the link below immediately to keep your account active.",

    actions: [
      "Report to Security Team",
      "Click the Link",
      "Reply to Sender",
      "Ignore the Email"
    ],

    correctAction: 0,

    explanation:
      "Suspicious password reset emails should always be reported to the organization's security team."
  },

  {
    id: 2,
    sender: "hr@midhani-careers.com",
    subject: "Updated Salary Details",

    body:
      "Please download the attached ZIP file containing your revised salary statement.",

    actions: [
      "Open the Attachment",
      "Forward to Friends",
      "Report to Security Team",
      "Reply with Personal Details"
    ],

    correctAction: 2,

    explanation:
      "Unexpected ZIP attachments are commonly used to distribute malware."
  },

  {
    id: 3,
    sender: "admin@midhani.in",
    subject: "Office 365 Login Required",

    body:
      "We detected unusual activity. Please log in again using the secure portal below.",

    actions: [
      "Click the Login Link",
      "Report to Security Team",
      "Reply Asking Questions",
      "Download the Attachment"
    ],

    correctAction: 1,

    explanation:
      "Never log in through links received in suspicious emails."
  }
];
export const completionSummary = {
  title: "Training Completed",

  message:
    "Congratulations! You have successfully completed the phishing awareness training module.",

  achievements: [
    "Identified common phishing red flags",
    "Analyzed realistic phishing emails",
    "Completed the phishing awareness quiz",
    "Practiced secure email decision making"
  ],

  reminders: [
    "Always verify the sender's email address.",
    "Do not click suspicious links or attachments.",
    "Never share passwords through email.",
    "Report suspicious emails to the security team."
  ]
};