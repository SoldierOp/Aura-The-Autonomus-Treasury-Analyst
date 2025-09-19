import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Upload, 
  FileSpreadsheet, 
  Download, 
  CheckCircle, 
  AlertCircle,
  ArrowRight,
  ArrowLeft,
  Settings,
  Filter,
  Calculator,
  BarChart3
} from 'lucide-react';

const InteractiveExcelProcessor = () => {
  const [currentStep, setCurrentStep] = useState('upload'); // upload, questions, processing, download
  const [fileId, setFileId] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [requirements, setRequirements] = useState({});
  const [processingResult, setProcessingResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (file) => {
    if (!file) return;

    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/analyze-excel/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze Excel file');
      }

      const result = await response.json();
      setFileId(result.file_id);
      setAnalysis(result.analysis);
      setCurrentStep('questions');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRequirementsSubmit = async () => {
    if (!fileId) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/process-excel-requirements/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          file_id: fileId,
          requirements: requirements
        })
      });

      if (!response.ok) {
        throw new Error('Failed to process Excel requirements');
      }

      const result = await response.json();
      setProcessingResult(result);
      setCurrentStep('download');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (processingResult?.download_file_id) {
      const downloadUrl = `http://localhost:8000/download-processed-excel/${processingResult.download_file_id}`;
      window.open(downloadUrl, '_blank');
    }
  };

  const handleRequirementChange = (questionId, value) => {
    setRequirements(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const renderUploadStep = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="text-center space-y-8"
    >
      <div className="space-y-4">
        <div className="w-24 h-24 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto">
          <FileSpreadsheet className="w-12 h-12 text-white" />
        </div>
        <h2 className="text-3xl font-bold text-gray-900">Interactive Excel Processor</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Upload your Excel file and I'll analyze it to ask you specific questions about what modifications you want.
        </p>
      </div>

      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 hover:border-blue-400 transition-colors">
        <input
          type="file"
          accept=".xlsx,.xls"
          onChange={(e) => handleFileUpload(e.target.files[0])}
          className="hidden"
          id="excel-upload"
        />
        <label
          htmlFor="excel-upload"
          className="cursor-pointer flex flex-col items-center space-y-4"
        >
          <Upload className="w-12 h-12 text-gray-400" />
          <div className="text-lg font-medium text-gray-700">
            {isLoading ? 'Analyzing Excel file...' : 'Click to upload Excel file'}
          </div>
          <div className="text-sm text-gray-500">
            Supports .xlsx and .xls formats
          </div>
        </label>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center space-x-3">
          <AlertCircle className="w-5 h-5 text-red-500" />
          <span className="text-red-700">{error}</span>
        </div>
      )}
    </motion.div>
  );

  const renderQuestionsStep = () => (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Customize Your Excel</h2>
          <p className="text-gray-600">Tell me what modifications you want</p>
        </div>
        <button
          onClick={() => setCurrentStep('upload')}
          className="flex items-center space-x-2 text-gray-500 hover:text-gray-700"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back</span>
        </button>
      </div>

      {analysis?.questions && (
        <div className="space-y-6">
          {analysis.questions.map((question, index) => (
            <motion.div
              key={question.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-lg border border-gray-200 p-6"
            >
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-blue-600 font-semibold text-sm">{index + 1}</span>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {question.question}
                    </h3>
                    
                    {question.type === 'multiple_choice' && (
                      <div className="space-y-2">
                        {question.options.map((option, optIndex) => (
                          <label key={optIndex} className="flex items-center space-x-3 cursor-pointer">
                            <input
                              type="radio"
                              name={question.id}
                              value={option}
                              onChange={(e) => handleRequirementChange(question.id, e.target.value)}
                              className="w-4 h-4 text-blue-600"
                            />
                            <span className="text-gray-700">{option}</span>
                          </label>
                        ))}
                      </div>
                    )}
                    
                    {question.type === 'yes_no' && (
                      <div className="flex space-x-4">
                        <label className="flex items-center space-x-2 cursor-pointer">
                          <input
                            type="radio"
                            name={question.id}
                            value="yes"
                            onChange={(e) => handleRequirementChange(question.id, e.target.value)}
                            className="w-4 h-4 text-blue-600"
                          />
                          <span className="text-gray-700">Yes</span>
                        </label>
                        <label className="flex items-center space-x-2 cursor-pointer">
                          <input
                            type="radio"
                            name={question.id}
                            value="no"
                            onChange={(e) => handleRequirementChange(question.id, e.target.value)}
                            className="w-4 h-4 text-blue-600"
                          />
                          <span className="text-gray-700">No</span>
                        </label>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      <div className="flex justify-end">
        <button
          onClick={handleRequirementsSubmit}
          disabled={isLoading}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center space-x-2"
        >
          {isLoading ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>Processing...</span>
            </>
          ) : (
            <>
              <span>Process Excel</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>
    </motion.div>
  );

  const renderDownloadStep = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="text-center space-y-8"
    >
      <div className="space-y-4">
        <div className="w-24 h-24 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto">
          <CheckCircle className="w-12 h-12 text-white" />
        </div>
        <h2 className="text-3xl font-bold text-gray-900">Excel Processed Successfully!</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Your Excel file has been modified according to your requirements. Download the processed file below.
        </p>
      </div>

      {processingResult && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 max-w-md mx-auto">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Processing Summary</h3>
          <div className="space-y-3 text-left">
            <div className="flex justify-between">
              <span className="text-gray-600">Original Rows:</span>
              <span className="font-semibold">{processingResult.file_info?.original_rows}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Modified Rows:</span>
              <span className="font-semibold">{processingResult.file_info?.modified_rows}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Sheets Processed:</span>
              <span className="font-semibold">{processingResult.file_info?.sheets_processed}</span>
            </div>
          </div>
          
          {processingResult.modifications_applied && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <h4 className="font-semibold text-gray-900 mb-2">Modifications Applied:</h4>
              <ul className="space-y-1">
                {processingResult.modifications_applied.map((mod, index) => (
                  <li key={index} className="text-sm text-gray-600 flex items-center">
                    <CheckCircle className="w-3 h-3 text-green-500 mr-2" />
                    {mod}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="flex space-x-4 justify-center">
        <button
          onClick={handleDownload}
          className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center space-x-2"
        >
          <Download className="w-4 h-4" />
          <span>Download Processed Excel</span>
        </button>
        <button
          onClick={() => {
            setCurrentStep('upload');
            setFileId(null);
            setAnalysis(null);
            setRequirements({});
            setProcessingResult(null);
          }}
          className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 flex items-center space-x-2"
        >
          <Upload className="w-4 h-4" />
          <span>Process Another File</span>
        </button>
      </div>
    </motion.div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12">
      <div className="max-w-4xl mx-auto px-6">
        {/* Progress Steps */}
        <div className="flex items-center justify-center mb-12">
          <div className="flex items-center space-x-4">
            {['upload', 'questions', 'processing', 'download'].map((step, index) => (
              <div key={step} className="flex items-center">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                  currentStep === step ? 'bg-blue-600 text-white' :
                  ['upload', 'questions', 'processing', 'download'].indexOf(currentStep) > index ? 'bg-green-500 text-white' :
                  'bg-gray-200 text-gray-500'
                }`}>
                  {step === 'upload' && <Upload className="w-5 h-5" />}
                  {step === 'questions' && <Settings className="w-5 h-5" />}
                  {step === 'processing' && <Calculator className="w-5 h-5" />}
                  {step === 'download' && <Download className="w-5 h-5" />}
                </div>
                {index < 3 && (
                  <div className={`w-12 h-1 mx-2 ${
                    ['upload', 'questions', 'processing', 'download'].indexOf(currentStep) > index ? 'bg-green-500' : 'bg-gray-200'
                  }`} />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <AnimatePresence mode="wait">
            {currentStep === 'upload' && renderUploadStep()}
            {currentStep === 'questions' && renderQuestionsStep()}
            {currentStep === 'download' && renderDownloadStep()}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

export default InteractiveExcelProcessor;
