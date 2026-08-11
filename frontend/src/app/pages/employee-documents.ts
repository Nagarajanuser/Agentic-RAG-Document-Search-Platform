import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface DocumentFile {
  name: string;
  category: string;
  uploadedDate: string;
  status: 'Verified' | 'Pending Verification' | 'Expired';
  size: string;
}

@Component({
  selector: 'app-employee-documents',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container-fluid py-4">
      <!-- Title -->
      <div class="d-flex align-items-center justify-content-between mb-4">
        <div>
          <h1 class="h3 mb-0 text-gray-800 fw-bold">Employee Documents</h1>
          <p class="text-muted small mb-0">Upload official documents, check verification statuses, and read handbook guidelines.</p>
        </div>
      </div>

      <div class="row g-4">
        <!-- Upload & List -->
        <div class="col-12 col-lg-8">
          <!-- Upload Area -->
          <div class="card border-0 shadow-sm rounded-3 p-4 bg-white mb-4">
            <h5 class="fw-bold mb-3 text-secondary"><i class="bi bi-cloud-arrow-up text-primary me-2"></i> Submit New Document</h5>
            
            <div class="border border-dashed border-primary border-2 bg-light-subtle rounded-3 p-4 text-center my-3" style="border-style: dashed !important; background-color: #f8fafc;">
              <i class="bi bi-file-earmark-arrow-up text-primary display-4 mb-2"></i>
              <h6 class="fw-bold mb-1">Select file to upload</h6>
              <p class="text-muted small mb-3">Acceptable formats: PDF, PNG, JPG up to 10MB</p>
              
              <!-- Simple Mock Upload Input -->
              <div class="d-inline-block">
                <input type="file" id="fileUpload" class="d-none" (change)="onFileSelected($event)">
                <label for="fileUpload" class="btn btn-primary btn-sm fw-bold px-4 cursor-pointer">
                  Browse Files
                </label>
              </div>
            </div>
          </div>

          <!-- Document List Table -->
          <div class="card border-0 shadow-sm rounded-3 p-4 bg-white">
            <h5 class="fw-bold mb-4 text-secondary"><i class="bi bi-file-earmark-medical text-primary me-2"></i> My Document Archive</h5>
            
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="table-light text-muted">
                  <tr>
                    <th>Document Name</th>
                    <th>Category</th>
                    <th>Uploaded Date</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr *ngFor="let doc of documents">
                    <td>
                      <div class="fw-semibold text-dark"><i class="bi bi-file-pdf text-danger me-2"></i>{{ doc.name }}</div>
                      <div class="small text-muted">{{ doc.size }}</div>
                    </td>
                    <td>{{ doc.category }}</td>
                    <td>{{ doc.uploadedDate }}</td>
                    <td>
                      <span class="badge rounded-pill" [ngClass]="{
                        'bg-success-subtle text-success': doc.status === 'Verified',
                        'bg-warning-subtle text-warning': doc.status === 'Pending Verification',
                        'bg-danger-subtle text-danger': doc.status === 'Expired'
                      }">{{ doc.status }}</span>
                    </td>
                    <td>
                      <button (click)="viewDoc(doc.name)" class="btn btn-sm btn-light border me-1" title="View">
                        <i class="bi bi-eye"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Corporate Handbooks -->
        <div class="col-12 col-lg-4">
          <div class="card border-0 shadow-sm rounded-3 p-4 bg-white h-100">
            <h5 class="fw-bold mb-4 text-secondary"><i class="bi bi-journal-bookmark text-primary me-2"></i> Company Handbooks</h5>
            <p class="text-muted small">Quick links to view or download global corporate policy guidelines:</p>
            
            <div class="list-group list-group-flush">
              <a href="javascript:void(0)" (click)="downloadHandbook('Employee Handbook 2026')" class="list-group-item list-group-item-action px-0 py-3 border-light-subtle d-flex align-items-center">
                <i class="bi bi-file-pdf text-danger fs-3 me-3"></i>
                <div>
                  <h6 class="mb-0 fw-bold text-dark small">Employee Handbook 2026</h6>
                  <span class="text-muted small">Updated: Jan 2026 • 2.4MB</span>
                </div>
              </a>
              
              <a href="javascript:void(0)" (click)="downloadHandbook('IT Security Policy')" class="list-group-item list-group-item-action px-0 py-3 border-light-subtle d-flex align-items-center">
                <i class="bi bi-file-pdf text-danger fs-3 me-3"></i>
                <div>
                  <h6 class="mb-0 fw-bold text-dark small">IT Security Policy</h6>
                  <span class="text-muted small">Updated: Nov 2025 • 1.1MB</span>
                </div>
              </a>

              <a href="javascript:void(0)" (click)="downloadHandbook('Code of Conduct & Ethics')" class="list-group-item list-group-item-action px-0 py-3 border-light-subtle d-flex align-items-center">
                <i class="bi bi-file-pdf text-danger fs-3 me-3"></i>
                <div>
                  <h6 class="mb-0 fw-bold text-dark small">Code of Conduct & Ethics</h6>
                  <span class="text-muted small">Updated: May 2025 • 850KB</span>
                </div>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class EmployeeDocumentsComponent {
  documents: DocumentFile[] = [
    { name: 'Signed_Employment_Contract.pdf', category: 'HR Agreements', uploadedDate: 'June 01, 2026', status: 'Verified', size: '1.2 MB' },
    { name: 'US_Federal_W-4_2026.pdf', category: 'Tax & Compliance', uploadedDate: 'June 02, 2026', status: 'Verified', size: '420 KB' },
    { name: 'Direct_Deposit_Chase_Authorization.pdf', category: 'Payroll & Banking', uploadedDate: 'June 03, 2026', status: 'Verified', size: '310 KB' },
    { name: 'US_Passport_Copy_2026.pdf', category: 'Identification', uploadedDate: 'June 01, 2026', status: 'Expired', size: '2.1 MB' }
  ];

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      const now = new Date();
      const dateStr = now.toLocaleDateString([], { year: 'numeric', month: 'short', day: '2-digit' });
      const sizeStr = (file.size / (1024 * 1024)).toFixed(1) + ' MB';
      
      const newDoc: DocumentFile = {
        name: file.name,
        category: 'Personal Upload',
        uploadedDate: dateStr,
        status: 'Pending Verification',
        size: sizeStr
      };

      this.documents = [newDoc, ...this.documents];
      alert(`Success: "${file.name}" uploaded successfully! It is now pending compliance review.`);
    }
  }

  viewDoc(name: string) {
    alert(`Opening document preview for "${name}"...`);
  }

  downloadHandbook(title: string) {
    alert(`Downloading handbook: "${title}"...`);
  }
}
