name: Bug Report
description: File a bug report for the financial reporting metrics backend platform
title: "[BUG] "
labels: ["bug", "triage"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        ## Bug Report
        Thank you for taking the time to file a bug report. Please fill out this form as completely as possible to help us investigate and resolve the issue efficiently.

  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: Provide a clear and concise description of the bug.
      placeholder: Describe the bug in detail...
    validations:
      required: true

  - type: textarea
    id: reproduction-steps
    attributes:
      label: Steps to Reproduce
      description: Provide detailed steps to reproduce the behavior.
      value: |
        1. Go to '...'
        2. Click on '...'
        3. Scroll down to '...'
        4. Observe the error
    validations:
      required: true

  - type: textarea
    id: expected-behavior
    attributes:
      label: Expected Behavior
      description: Describe what you expected to happen.
      placeholder: I expected that...
    validations:
      required: true

  - type: textarea
    id: actual-behavior
    attributes:
      label: Actual Behavior
      description: Describe what actually happened.
      placeholder: Instead, what happened was...
    validations:
      required: true

  - type: dropdown
    id: environment
    attributes:
      label: Environment
      description: Specify the environment where the bug occurred.
      options:
        - Production
        - Staging
        - Development
        - Local
    validations:
      required: true

  - type: input
    id: api-endpoint
    attributes:
      label: API Endpoint
      description: If applicable, provide the API endpoint related to this bug.
      placeholder: e.g., /api/v1/companies

  - type: input
    id: version
    attributes:
      label: Version
      description: Specify the version of the application where the bug occurred.
      placeholder: e.g., v1.2.3

  - type: textarea
    id: error-message
    attributes:
      label: Error Message
      description: If applicable, provide the full error message or stack trace.
      render: shell

  - type: textarea
    id: additional-context
    attributes:
      label: Additional Context
      description: Add any other context about the problem here. This may include screenshots, logs, or related information.

  - type: checkboxes
    id: confirmations
    attributes:
      label: Confirmations
      description: Please confirm the following before submitting the bug report.
      options:
        - label: I have checked that this bug has not been reported before.
          required: true
        - label: I have included all the necessary information to reproduce this bug.
          required: true
        - label: I have removed any sensitive information from my submission.
          required: true

  - type: markdown
    attributes:
      value: |
        ## Thank You
        Thank you for taking the time to fill out this bug report. Your detailed information helps us improve the quality of our financial reporting metrics backend platform.
        
        For more information on our bug reporting process, please refer to the [Technical Specification/System Architecture/CI/CD Pipeline] section of our documentation.

        If you have any questions about this form, please contact the development team.