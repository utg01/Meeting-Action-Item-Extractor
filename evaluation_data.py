evaluation_data_list = [

    {
        "name": "Pricing and Presentation Meeting",

        "transcript": """
Alice: We need to update the pricing page by Thursday.
Sarah: I'll handle that.

Bob: I'll prepare the technical slides by Wednesday.
Sarah: I'll prepare the marketing slides by Wednesday.

Alice: Bob, can you test the homepage on both mobile and desktop by Friday?
Bob: Yes, I'll do it.
""",

        "ground_truth": [
            {
                "task": "Update the pricing page",
                "owner": "Sarah",
                "deadline": "Thursday",
                "status": "pending"
            },
            {
                "task": "Prepare the technical slides",
                "owner": "Bob",
                "deadline": "Wednesday",
                "status": "pending"
            },
            {
                "task": "Prepare the marketing slides",
                "owner": "Sarah",
                "deadline": "Wednesday",
                "status": "pending"
            },
            {
                "task": "Test the homepage on both mobile and desktop",
                "owner": "Bob",
                "deadline": "Friday",
                "status": "pending"
            }
        ]
    },


    {
        "name": "Customer Feedback Meeting",

        "transcript": """
Alice: The homepage redesign is complete.

Bob: Great. I'll upload the final screenshots by Friday.

Sarah: I'll prepare the customer feedback form by Sunday.

Bob: Once Sarah finishes it, I'll test the form.

Alice: I'll prepare the backup plan.

Sarah: I'll send the customer communication after Alice approves the email.
""",

        "ground_truth": [
            {
                "task": "Upload the final screenshots",
                "owner": "Bob",
                "deadline": "Friday",
                "status": "pending"
            },
            {
                "task": "Prepare the customer feedback form",
                "owner": "Sarah",
                "deadline": "Sunday",
                "status": "pending"
            },
            {
                "task": "Test the customer feedback form",
                "owner": "Bob",
                "deadline": None,
                "status": "pending"
            },
            {
                "task": "Prepare the backup plan",
                "owner": "Alice",
                "deadline": None,
                "status": "pending"
            },
            {
                "task": "Send the customer communication",
                "owner": "Sarah",
                "deadline": None,
                "status": "pending"
            }
        ]
    },


    {
        "name": "Payment and Launch Meeting",

        "transcript": """
Alice: The payment integration testing is complete.

Bob: I still need to test the refund and cancelled transaction cases today.

Sarah: I'll update the social media posts by Wednesday.

Alice: The launch email first draft needs to be ready by Tuesday.

Bob: I'll review the draft once it is ready.
""",

        "ground_truth": [
            {
                "task": "Test the refund and cancelled transaction cases",
                "owner": "Bob",
                "deadline": "today",
                "status": "pending"
            },
            {
                "task": "Update the social media posts",
                "owner": "Sarah",
                "deadline": "Wednesday",
                "status": "pending"
            },
            {
                "task": "Prepare the launch email first draft",
                "owner": "Alice",
                "deadline": "Tuesday",
                "status": "pending"
            },
            {
                "task": "Review the launch email draft",
                "owner": "Bob",
                "deadline": None,
                "status": "pending"
            }
        ]
    },


    {
        "name": "Technical Tasks Meeting",

        "transcript": """
Alice: Bob, please investigate the duplicate signup event.

Bob: I'll investigate and fix it by Friday.

Sarah: I'll check the pricing page on mobile.

Alice: The database restoration test should be completed by Friday.

Bob: I'll take care of that.

Sarah: I'll prepare the marketing slides by Wednesday.
""",

        "ground_truth": [
            {
                "task": "Investigate and fix the duplicate signup event",
                "owner": "Bob",
                "deadline": "Friday",
                "status": "pending"
            },
            {
                "task": "Check the pricing page on mobile",
                "owner": "Sarah",
                "deadline": None,
                "status": "pending"
            },
            {
                "task": "Perform the database restoration test",
                "owner": "Bob",
                "deadline": "Friday",
                "status": "pending"
            },
            {
                "task": "Prepare the marketing slides",
                "owner": "Sarah",
                "deadline": "Wednesday",
                "status": "pending"
            }
        ]
    },


    {
        "name": "Launch Preparation Meeting",

        "transcript": """
Alice: The customer email has already been sent.

Bob: The application logs need to be monitored on the first day after launch.

Sarah: I'll handle the final customer communication after Alice approves the email.

Alice: I'll review the first draft tomorrow.

Bob: I'll test the homepage on mobile and desktop by Friday.
""",

        "ground_truth": [
            {
                "task": "Monitor the application logs on the first day after launch",
                "owner": "Bob",
                "deadline": None,
                "status": "pending"
            },
            {
                "task": "Send the final customer communication",
                "owner": "Sarah",
                "deadline": None,
                "status": "pending"
            },
            {
                "task": "Review the first draft",
                "owner": "Alice",
                "deadline": "tomorrow",
                "status": "pending"
            },
            {
                "task": "Test the homepage on mobile and desktop",
                "owner": "Bob",
                "deadline": "Friday",
                "status": "pending"
            }
        ]
    }
]






sample_transcripts = {

    "Software Development Meeting": """
Alice: We need to fix the login bug before Friday.
Bob: I'll investigate the issue and fix it.

Sarah: I'll update the documentation by Monday.

Alice: Bob, please test the login flow after the fix.
Bob: Sure, I'll test it.
""",

    "Marketing Meeting": """
Sarah: I'll prepare the Instagram campaign by Wednesday.

Alice: Please also prepare the email newsletter.
Sarah: I'll send the first draft tomorrow.

Bob: I'll review the campaign analytics next week.
""",

    "Project Planning Meeting": """
Alice: We need to finalize the project timeline by Friday.

Bob: I'll prepare the technical plan by Thursday.

Sarah: I'll prepare the presentation slides by Monday.

Alice: Bob, please review the timeline once it's ready.
""",

    "Client Meeting": """
Client: We need the revised proposal by Tuesday.

Alice: I'll prepare the revised proposal.

Bob: I'll review the pricing section before we send it.

Sarah: I'll prepare the supporting documents by Monday.
"""
}