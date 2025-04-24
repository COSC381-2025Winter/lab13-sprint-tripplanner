name:  Feature Request
description: Suggest a new feature or improvement.
title: "[FEATURE] "
labels: enhancement
body:
  - type: textarea
    id: proposal
    attributes:
      label: Describe the feature
      description: What would you like to see added or changed?
      placeholder: I think it would be helpful if...
    validations:
      required: true

  - type: textarea
    id: use_case
    attributes:
      label: Why is this feature important?
      description: What problem does it solve or what value does it add?
      placeholder: This would make it easier for users to...

  - type: textarea
    id: additional
    attributes:
      label: Additional context (optional)
      description: Anything else you want to add? Screenshots? Links? Mockups?
