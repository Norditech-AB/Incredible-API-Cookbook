<!-- Code Example Template with Tabs -->
<!-- Include the CSS/JS only once per page -->
<script>
if (!window.codeTabsLoaded) {
  document.head.insertAdjacentHTML('beforeend', `
    <style>
    .code-tabs {
      margin: 20px 0;
      border: 1px solid #e1e4e8;
      border-radius: 6px;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    }

    .code-tabs-header {
      background-color: #f6f8fa;
      border-bottom: 1px solid #e1e4e8;
      display: flex;
      margin: 0;
      padding: 0;
    }

    .code-tab-button {
      background: none;
      border: none;
      padding: 12px 16px;
      cursor: pointer;
      font-size: 14px;
      font-weight: 500;
      color: #586069;
      border-bottom: 2px solid transparent;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
      user-select: none;
    }

    .code-tab-button:hover {
      background-color: #e1e4e8;
      color: #24292e;
    }

    .code-tab-button.active {
      color: #0366d6;
      border-bottom-color: #0366d6;
      background-color: #ffffff;
    }

    .code-tab-button::before {
      content: '';
      display: inline-block;
      width: 16px;
      height: 16px;
      background-size: contain;
      background-repeat: no-repeat;
      flex-shrink: 0;
    }

    .code-tab-button[data-language="python"]::before {
      background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23306998"><path d="M14.25.18l.9.2.73.26.59.3.45.32.34.34.25.34.16.33.1.3.04.26.02.2-.01.13V8.5l-.05.63-.13.55-.21.46-.26.38-.3.31-.33.25-.35.19-.35.14-.33.1-.3.07-.26.04-.21.02H8.77l-.69.05-.59.14-.5.22-.41.27-.33.32-.27.35-.2.36-.15.37-.1.35-.07.32-.04.27-.02.21v3.06H3.17l-.21-.03-.28-.07-.32-.12-.35-.18-.36-.26-.36-.36-.35-.46-.32-.59-.28-.73-.21-.88-.14-1.05-.05-1.23.06-1.22.16-1.04.24-.87.32-.71.36-.57.4-.44.42-.33.42-.24.4-.16.36-.1.32-.05.24-.01h.16l.06.01h8.16v-.83H6.18l-.01-2.75-.02-.37.05-.34.11-.31.17-.28.25-.26.31-.23.38-.2.44-.18.51-.15.58-.12.64-.1.71-.06.77-.04.84-.02 1.27.05zm-6.3 1.98l-.23.33-.08.41.08.41.23.34.33.22.41.09.41-.09.33-.22.23-.34.08-.41-.08-.41-.23-.33-.33-.22-.41-.09-.41.09-.33.22zM21.1 6.11l.28.06.32.12.35.18.36.27.36.35.35.47.32.59.28.73.21.88.14 1.04.05 1.23-.06 1.23-.16 1.04-.24.86-.32.71-.36.57-.4.45-.42.33-.42.24-.4.16-.36.09-.32.05-.24.02-.16-.01h-8.22v.82h5.84l.01 2.76.02.36-.05.34-.11.31-.17.29-.25.25-.31.24-.38.2-.44.17-.51.15-.58.13-.64.09-.71.07-.77.04-.84.01-1.27-.04-1.07-.14-.9-.2-.73-.25-.59-.3-.45-.33-.34-.34-.25-.34-.16-.33-.1-.3-.04-.25-.02-.2.01-.13v-5.34l.05-.64.13-.54.21-.46.26-.38.3-.32.33-.24.35-.2.35-.14.33-.1.3-.06.26-.04.21-.02.13-.01h5.84l.69-.05.59-.14.5-.21.41-.28.33-.32.27-.35.2-.36.15-.36.1-.35.07-.32.04-.28.02-.21V6.07h2.09l.14.01zm-6.47 14.25l-.23.33-.08.41.08.41.23.33.33.23.41.08.41-.08.33-.23.23-.33.08-.41-.08-.41-.23-.33-.33-.23-.41-.08-.41.08-.33.23z"/></svg>');
    }

    .code-tab-button[data-language="javascript"]::before {
      background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23f7df1e"><path d="M0 0h24v24H0V0zm22.034 18.276c-.175-1.095-.888-2.015-3.003-2.873-.736-.345-1.554-.585-1.797-1.14-.091-.33-.105-.51-.046-.705.15-.646.915-.84 1.515-.66.39.12.75.42.976.9 1.034-.676 1.034-.676 1.755-1.125-.27-.42-.404-.601-.586-.78-.63-.705-1.469-1.065-2.834-1.034l-.705.089c-.676.165-1.32.525-1.71 1.005-1.14 1.291-.811 3.541.569 4.471 1.365 1.02 3.361 1.244 3.616 2.205.24 1.17-.87 1.545-1.966 1.41-.811-.18-1.26-.586-1.755-1.336l-1.83 1.051c.21.48.45.689.81 1.109 1.74 1.756 6.09 1.666 6.871-1.004.029-.09.24-.705.074-1.65l.046.067zm-8.983-7.245h-2.248c0 1.938-.009 3.864-.009 5.805 0 1.232.063 2.363-.138 2.711-.33.689-1.18.601-1.566.48-.396-.196-.597-.466-.83-.855-.063-.105-.11-.196-.127-.196l-1.825 1.125c.305.63.75 1.172 1.324 1.517.855.51 2.004.675 3.207.405.783-.226 1.458-.691 1.811-1.411.51-.93.402-2.07.397-3.346.012-2.054 0-4.109 0-6.179l.004-.056z"/></svg>');
    }

    .code-tab-button[data-language="bash"]::before {
      background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23333"><path d="M4 2h16c1.1 0 2 .9 2 2v16c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2zm0 2v16h16V4H4zm2 2h12v2H6V6zm0 4h8v2H6v-2zm0 4h12v2H6v-2z"/></svg>');
    }

    .code-tab-content {
      display: none;
      padding: 0;
      margin: 0;
      background-color: #ffffff;
    }

    .code-tab-content.active {
      display: block;
    }

    .code-tab-content pre {
      margin: 0;
      padding: 16px;
      background-color: #f6f8fa;
      border: none;
      border-radius: 0;
      overflow-x: auto;
      font-family: SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
    }

    .code-tab-content code {
      background-color: transparent;
      padding: 0;
      border-radius: 0;
      font-size: 14px;
      line-height: 1.5;
      font-family: inherit;
    }

    .code-tab-header-controls {
      margin-left: auto;
      display: flex;
      align-items: center;
      padding-right: 8px;
    }

    .copy-button {
      background: none;
      border: 1px solid #e1e4e8;
      border-radius: 4px;
      padding: 4px 8px;
      font-size: 12px;
      color: #586069;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .copy-button:hover {
      background-color: #e1e4e8;
    }

    .copy-button.copied {
      color: #28a745;
      border-color: #28a745;
    }

    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
      .code-tabs {
        border-color: #30363d;
      }
      
      .code-tabs-header {
        background-color: #21262d;
        border-bottom-color: #30363d;
      }
      
      .code-tab-button {
        color: #8b949e;
      }
      
      .code-tab-button:hover {
        background-color: #30363d;
        color: #f0f6fc;
      }
      
      .code-tab-button.active {
        color: #58a6ff;
        background-color: #0d1117;
        border-bottom-color: #58a6ff;
      }
      
      .code-tab-content pre {
        background-color: #161b22;
        color: #e6edf3;
      }
      
      .copy-button {
        border-color: #30363d;
        color: #8b949e;
      }
      
      .copy-button:hover {
        background-color: #30363d;
      }
    }

    /* Responsive design */
    @media (max-width: 768px) {
      .code-tab-button {
        padding: 10px 12px;
        font-size: 13px;
      }
      
      .code-tab-content pre {
        padding: 12px;
        font-size: 13px;
      }
    }
    </style>
  `);
  
  window.codeTabsLoaded = true;
}

// JavaScript functionality
function initializeCodeTabs() {
  const codeTabs = document.querySelectorAll('.code-tabs:not(.initialized)');
  
  codeTabs.forEach(function(tabContainer) {
    tabContainer.classList.add('initialized');
    const buttons = tabContainer.querySelectorAll('.code-tab-button');
    const contents = tabContainer.querySelectorAll('.code-tab-content');
    
    // Set first tab as active by default (Python)
    if (buttons.length > 0) {
      buttons[0].classList.add('active');
      contents[0].classList.add('active');
    }
    
    // Add click listeners to tab buttons
    buttons.forEach(function(button, index) {
      button.addEventListener('click', function() {
        // Remove active class from all buttons and contents
        buttons.forEach(btn => btn.classList.remove('active'));
        contents.forEach(content => content.classList.remove('active'));
        
        // Add active class to clicked button and corresponding content
        button.classList.add('active');
        contents[index].classList.add('active');
      });
    });
  });
  
  // Copy button functionality
  const copyButtons = document.querySelectorAll('.copy-button:not(.initialized)');
  copyButtons.forEach(function(button) {
    button.classList.add('initialized');
    button.addEventListener('click', function() {
      const tabContent = button.closest('.code-tabs').querySelector('.code-tab-content.active pre code');
      const text = tabContent.textContent;
      
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
          button.textContent = 'Copied!';
          button.classList.add('copied');
          
          setTimeout(function() {
            button.textContent = 'Copy';
            button.classList.remove('copied');
          }, 2000);
        });
      } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        button.textContent = 'Copied!';
        setTimeout(function() {
          button.textContent = 'Copy';
        }, 2000);
      }
    });
  });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeCodeTabs);
} else {
  initializeCodeTabs();
}

// Also initialize after a short delay to catch dynamically loaded content
setTimeout(initializeCodeTabs, 100);
</script>
